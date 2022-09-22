import dataclasses
from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from django.contrib.auth.models import AbstractUser

from baserow.contrib.database.fields.backup_handler import (
    BackupData,
    FieldDataBackupHandler,
)
from baserow.contrib.database.fields.handler import FieldHandler
from baserow.contrib.database.fields.models import Field, SpecificFieldForUpdate
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.table.models import Table
from baserow.contrib.database.table.scopes import TableActionScopeType
from baserow.core.action.models import Action
from baserow.core.action.registries import ActionScopeStr, ActionType
from baserow.core.trash.handler import TrashHandler
from baserow.core.utils import ChildProgressBuilder


class UpdateFieldActionType(ActionType):
    type = "update_field"

    @dataclasses.dataclass
    class Params:
        field_id: int
        # We also need to persist the actual name of the database table in-case the
        # field itself is perm deleted by the time we clean up we can still find the
        # table and delete the column if need be.
        database_table_name: str

        previous_field_type: str
        previous_field_params: Dict[str, Any]

        backup_data: Optional[Dict[str, Any]]

    @classmethod
    def do(
        cls,
        user: AbstractUser,
        field: SpecificFieldForUpdate,
        new_type_name: Optional[str] = None,
        **kwargs,
    ) -> Tuple[Field, List[Field]]:

        """
        Updates the values and/or type of the given field. See
        baserow.contrib.database.fields.handler.FieldHandler.update_field for further
        details. Backs up the field attributes and data so undo will restore the
        original field and its data. Redo reapplies the update.

        :param user: The user on whose behalf the table is updated.
        :param field: The field instance that needs to be updated.
        :param new_type_name: If the type needs to be changed it can be provided here.
        :return: The updated field instance and any
            updated fields as a result of updated the field are returned in a list
            as the second tuple value.
        """

        from_field_type = field_type_registry.get_by_model(field)
        from_field_type_name = from_field_type.type
        to_field_type_name = new_type_name or from_field_type_name

        original_exported_values = cls._get_prepared_field_attrs(
            field, kwargs, to_field_type_name
        )

        # We initially create the action with blank params so we have an action id
        # to use when naming a possible backup field/table.
        action = cls.register_action(user, {}, cls.scope(field.table_id))

        optional_backup_data = cls._backup_field_if_required(
            field, kwargs, action, to_field_type_name, False
        )

        field, updated_fields = FieldHandler().update_field(
            user,
            field,
            new_type_name,
            return_updated_fields=True,
            **kwargs,
        )

        action.params = cls.Params(
            field_id=field.id,
            database_table_name=field.table.get_database_table_name(),
            previous_field_type=from_field_type_name,
            previous_field_params=original_exported_values,
            backup_data=optional_backup_data,
        )
        action.save()

        return field, updated_fields

    @classmethod
    def scope(cls, table_id) -> ActionScopeStr:
        return TableActionScopeType.value(table_id)

    @classmethod
    def undo(
        cls,
        user: AbstractUser,
        params: Params,
        action_being_undone: Action,
    ):
        cls._backup_field_then_update_back_to_previous_backup(
            user,
            action_being_undone,
            params,
            for_undo=True,
        )

    @classmethod
    def redo(cls, user: AbstractUser, params: Params, action_being_redone: Action):
        cls._backup_field_then_update_back_to_previous_backup(
            user,
            action_being_redone,
            params,
            for_undo=False,
        )

    @classmethod
    def clean_up_any_extra_action_data(cls, action_being_cleaned_up: Action):
        params = cls.Params(**action_being_cleaned_up.params)
        if params.backup_data is not None:
            FieldDataBackupHandler.clean_up_backup_data(params.backup_data)

    @classmethod
    def _backup_field_if_required(
        cls,
        original_field: Field,
        allowed_new_field_attrs: Dict[str, Any],
        action: Action,
        to_field_type_name: str,
        for_undo: bool,
    ) -> Optional[BackupData]:
        """
        Performs a backup if needed and returns a dictionary of backup data which can
        be then used with the FieldDataBackupHandler to restore a backup or clean up
        the backed up data.
        """

        if cls._should_backup_field(
            original_field, to_field_type_name, allowed_new_field_attrs
        ):
            backup_data = FieldDataBackupHandler.backup_field_data(
                original_field,
                identifier_to_backup_into=cls._get_backup_identifier(
                    action, original_field.id, for_undo=for_undo
                ),
            )
        else:
            backup_data = None
        return backup_data

    @classmethod
    def _should_backup_field(
        cls,
        original_field: Field,
        to_field_type_name: str,
        allowed_new_field_attrs: Dict[str, Any],
    ) -> bool:
        """
        Calculates whether the field should be backed up given its original instance,
        the type it is being converted to and any attributes which are being updated.
        """

        from_field_type = field_type_registry.get_by_model(original_field)
        from_field_type_name = from_field_type.type

        field_type_changed = to_field_type_name != from_field_type_name
        only_name_changed = allowed_new_field_attrs.keys() == {"name"}

        if from_field_type.field_data_is_derived_from_attrs:
            # If the field we are converting from can reconstruct its data just from its
            # attributes we never need to backup any data.
            return False

        return field_type_changed or (
            from_field_type.should_backup_field_data_for_same_type_update(
                original_field, allowed_new_field_attrs
            )
            and not only_name_changed
        )

    @classmethod
    def _get_prepared_field_attrs(
        cls, field: Field, field_attrs_being_updated: Set[str], to_field_type_name: str
    ):
        """
        Prepare values to be saved depending on whether the field type has changed
        or not.

        If we aren't changing field type then only save the attributes which
        the user has changed.

        Otherwise, if we have changed field type then we need to save all the original
        field types attributes. However we don't want to save the only shared
        field attr "name" if it hasn't changed so we don't undo other users name
        changes.
        """

        from_field_type = field_type_registry.get_by_model(field)
        from_field_type_name = from_field_type.type

        original_exported_values = from_field_type.export_prepared_values(field)
        if to_field_type_name == from_field_type_name:
            exported_field_attrs_which_havent_changed = (
                original_exported_values.keys() - field_attrs_being_updated
            )
            for key in exported_field_attrs_which_havent_changed:
                original_exported_values.pop(key)
        else:
            if "name" not in field_attrs_being_updated:
                original_exported_values.pop("name")
        return original_exported_values

    @classmethod
    def _get_backup_identifier(
        cls, action: Action, field_id: int, for_undo: bool
    ) -> str:
        """
        Returns a column/table name unique to this action and field which can be
        used to safely store backup data in the database.
        """

        base_name = f"field_{field_id}_backup_{action.id}"
        if for_undo:
            # When undoing we need to backup into a different column/table so we
            # don't accidentally overwrite the data we are about to restore using.
            return base_name + "_undo"
        else:
            return base_name

    @classmethod
    def _backup_field_then_update_back_to_previous_backup(
        cls,
        user: AbstractUser,
        action: Action,
        params: Params,
        for_undo: bool,
    ):
        new_field_attributes = deepcopy(params.previous_field_params)
        to_field_type_name = params.previous_field_type

        handler = FieldHandler()
        field = handler.get_specific_field_for_update(params.field_id)

        updated_field_attrs = set(new_field_attributes.keys())
        previous_field_params = cls._get_prepared_field_attrs(
            field, updated_field_attrs, to_field_type_name
        )
        from_field_type = field_type_registry.get_by_model(field)
        from_field_type_name = from_field_type.type

        optional_backup_data = cls._backup_field_if_required(
            field, new_field_attributes, action, to_field_type_name, for_undo
        )

        def after_field_schema_change_callback(
            field_after_schema_change: SpecificFieldForUpdate,
        ):
            if params.backup_data:
                # We have to restore the field data immediately after the schema change
                # as the dependant field updates performed by `update_field` need the
                # correct cell data in place and ready.
                # E.g. If the field we are undoing has a formula field which depends
                # on it we have to copy back in the cell values before that formula
                # field updates its own cells.
                FieldDataBackupHandler.restore_backup_data_into_field(
                    field_after_schema_change, params.backup_data
                )

        # If when undoing/redoing there is now a new field with the same name we don't
        # want to fail and throw away all the users lost data. Instead we just find
        # a new free field name starting by adding the following postfix on and use
        # that instead.
        collision_postfix = "(From undo)" if for_undo else "(From redo)"
        handler.update_field(
            user,
            field,
            new_type_name=to_field_type_name,
            postfix_to_fix_name_collisions=collision_postfix,
            return_updated_fields=True,
            after_schema_change_callback=after_field_schema_change_callback,
            **new_field_attributes,
        )

        params.backup_data = optional_backup_data
        params.previous_field_type = from_field_type_name
        params.previous_field_params = previous_field_params
        action.params = params


class CreateFieldActionType(ActionType):
    type = "create_field"

    @dataclasses.dataclass
    class Params:
        field_id: int

    @classmethod
    def do(
        cls,
        user: AbstractUser,
        table: Table,
        type_name: str,
        primary=False,
        return_updated_fields=False,
        **kwargs,
    ) -> Union[Field, Tuple[Field, List[Field]]]:
        """
        Creates a new field with the given type for a table.
        See baserow.contrib.database.fields.handler.FieldHandler.create_field()
        for more information.
        Undoing this action will delete the field.
        Redoing this action will restore the field.

        :param user: The user on whose behalf the field is created.
        :param table: The table that the field belongs to.
        :param type_name: The type name of the field. Available types can be found in
            the field_type_registry.
        :param primary: Every table needs at least a primary field which cannot be
            deleted and is a representation of the whole row.
        :param return_updated_fields: When True any other fields who changed as a
            result of this field creation are returned with their new field instances.
        :param kwargs: The field values that need to be set upon creation.
        :type kwargs: object
        :return: The created field instance. If return_updated_field is set then any
            updated fields as a result of creating the field are returned in a list
            as a second tuple value.
        """

        result = FieldHandler().create_field(
            user,
            table,
            type_name,
            primary=primary,
            return_updated_fields=return_updated_fields,
            **kwargs,
        )

        if return_updated_fields:
            field, updated_fields = result
        else:
            field = result
            updated_fields = None

        cls.register_action(
            user=user, params=cls.Params(field_id=field.id), scope=cls.scope(table.id)
        )

        return (field, updated_fields) if return_updated_fields else field

    @classmethod
    def scope(cls, table_id) -> ActionScopeStr:
        return TableActionScopeType.value(table_id)

    @classmethod
    def undo(cls, user: AbstractUser, params: Params, action_being_undone: Action):
        field = FieldHandler().get_field(params.field_id)
        FieldHandler().delete_field(user, field)

    @classmethod
    def redo(cls, user: AbstractUser, params: Params, action_being_redone: Action):
        TrashHandler().restore_item(user, "field", params.field_id)


class DeleteFieldActionType(ActionType):
    type = "delete_field"

    @dataclasses.dataclass
    class Params:
        field_id: int

    @classmethod
    def do(
        cls,
        user: AbstractUser,
        field: Field,
    ) -> List[Field]:
        """
        Deletes an existing field if it is not a primary field.
        See baserow.contrib.database.fields.handler.FieldHandler.delete_field()
        for more information.
        Undoing this action will restore the field.
        Redoing this action will delete the field.

        :param user: The user on whose behalf the table is created.
        :param field: The field instance that needs to be deleted.
        :return: The related updated fields.
        """

        result = FieldHandler().delete_field(user, field)

        cls.register_action(
            user=user,
            params=cls.Params(
                field.id,
            ),
            scope=cls.scope(field.table_id),
        )

        return result

    @classmethod
    def scope(cls, table_id) -> ActionScopeStr:
        return TableActionScopeType.value(table_id)

    @classmethod
    def undo(cls, user: AbstractUser, params: Params, action_being_undone: Action):
        TrashHandler().restore_item(user, "field", params.field_id)

    @classmethod
    def redo(cls, user: AbstractUser, params: Params, action_being_redone: Action):
        field = FieldHandler().get_field(params.field_id)
        FieldHandler().delete_field(
            user,
            field,
        )


class DuplicateFieldActionType(ActionType):
    type = "duplicate_field"

    @dataclasses.dataclass
    class Params:
        field_id: int

    @classmethod
    def do(
        cls,
        user: AbstractUser,
        field: Field,
        duplicate_data: bool = False,
        progress_builder: Optional[ChildProgressBuilder] = None,
    ) -> Tuple[Field, List[Field]]:
        """
        Duplicate a field. Undoing this action trashes the duplicated field and
        redoing restores it.

        :param user: The user on whose behalf the duplicated field will be
            created.
        :param field: The field instance to duplicate.
        :param progress_builder: A progress builder instance that can be used to
            track the progress of the duplication.
        :return: A tuple with duplicated field instance and a list of the fields
            that have been updated.
        """

        new_field_clone, updated_fields = FieldHandler().duplicate_field(
            user, field, duplicate_data, progress_builder=progress_builder
        )
        cls.register_action(
            user, cls.Params(new_field_clone.id), cls.scope(field.table_id)
        )
        return new_field_clone, updated_fields

    @classmethod
    def scope(cls, table_id) -> ActionScopeStr:
        return TableActionScopeType.value(table_id)

    @classmethod
    def undo(cls, user: AbstractUser, params: Params, action_being_undone: Action):
        FieldHandler().delete_field(user, FieldHandler().get_field(params.field_id))

    @classmethod
    def redo(cls, user: AbstractUser, params: Params, action_being_redone: Action):
        TrashHandler.restore_item(
            user, "field", params.field_id, parent_trash_item_id=None
        )
