import dataclasses
from typing import Any, List, Optional

from django.contrib.auth.models import AbstractUser

from baserow.core.action.models import Action
from baserow.core.action.registries import ActionScopeStr, UndoRedoActionType
from baserow.core.action.scopes import GroupActionScopeType, RootActionScopeType
from baserow.core.handler import CoreHandler, GroupForUpdate
from baserow.core.models import Application, Group, GroupUser, Template
from baserow.core.registries import application_type_registry
from baserow.core.trash.handler import TrashHandler
from baserow.core.utils import ChildProgressBuilder

from django.utils.translation import gettext as _


class DeleteGroupActionType(UndoRedoActionType):
    type = "delete_group"

    @dataclasses.dataclass
    class Params:
        group_id: int
        group_name: str

    def do(cls, user: AbstractUser, group: GroupForUpdate):
        """
        Deletes an existing group and related applications if the user has admin
        permissions for the group. See baserow.core.handler.CoreHandler.delete_group
        for more details. Undoing this action restores the group, redoing it deletes it
        again.

        :param user: The user performing the delete.
        :param group: A LockedGroup obtained from CoreHandler.get_group_for_update which
            will be deleted.
        """

        CoreHandler().delete_group(user, group)

        cls.register_action(user, cls.Params(group.id, group.name), scope=cls.scope())

    @classmethod
    def scope(cls) -> ActionScopeStr:
        return RootActionScopeType.value()

    @classmethod
    def undo(
        cls,
        user: AbstractUser,
        params: Params,
        action_to_undo: Action,
    ):
        TrashHandler.restore_item(
            user,
            "group",
            params.group_id,
        )

    @classmethod
    def redo(
        cls,
        user: AbstractUser,
        params: Params,
        action_to_redo: Action,
    ):
        CoreHandler().delete_group_by_id(user, params.group_id)

    @classmethod
    def get_action_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _('Group "%(group_name)s" (%(group_id)s) deleted') % {
            "group_name": params.group_name,
            "group_id": params.group_id,
        }

    @classmethod
    def get_type_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _("Group deleted")


class CreateGroupActionType(UndoRedoActionType):
    type = "create_group"

    @dataclasses.dataclass
    class Params:
        group_id: int
        group_name: str

    @classmethod
    def do(cls, user: AbstractUser, group_name: str) -> GroupUser:
        """
        Creates a new group for an existing user. See
        baserow.core.handler.CoreHandler.create_group for more details. Undoing this
        action deletes the created group, redoing it restores it from the trash.

        :param user: The user creating the group.
        :param group_name: The name to give the group.
        """

        group_user = CoreHandler().create_group(user, name=group_name)
        group = group_user.group

        cls.register_action(
            user=user,
            params=cls.Params(group.id, group_name),
            scope=cls.scope(),
        )
        return group_user

    @classmethod
    def scope(cls) -> ActionScopeStr:
        return RootActionScopeType.value()

    @classmethod
    def undo(
        cls,
        user: AbstractUser,
        params: Params,
        action_to_undo: Action,
    ):
        CoreHandler().delete_group_by_id(user, params.group_id)

    @classmethod
    def redo(
        cls,
        user: AbstractUser,
        params: Params,
        action_to_redo: Action,
    ):
        TrashHandler.restore_item(
            user, "group", params.group_id, parent_trash_item_id=None
        )

    @classmethod
    def get_action_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _('Created group "%(group_name)s" (%(group_id)s)') % {
            "group_name": params.group_name,
            "group_id": params.group_id,
        }

    @classmethod
    def get_type_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _("Group created")


class UpdateGroupActionType(UndoRedoActionType):
    type = "update_group"

    @dataclasses.dataclass
    class Params:
        group_id: int
        group_name: str
        original_group_name: str

    @classmethod
    def do(
        cls, user: AbstractUser, group: GroupForUpdate, new_group_name: str
    ) -> GroupForUpdate:
        """
        Updates the values of a group if the user has admin permissions to the group.
        See baserow.core.handler.CoreHandler.upgrade_group for more details. Undoing
        this action restores the name of the group prior to this action being performed,
        redoing this restores the new name set initially.

        :param user: The user creating the group.
        :param group: A LockedGroup obtained from CoreHandler.get_group_for_update on
            which the update will be run.
        :param new_group_name: The new name to give the group.
        :return: The updated group.
        """

        original_group_name = group.name
        CoreHandler().update_group(user, group, name=new_group_name)

        cls.register_action(
            user=user,
            params=cls.Params(
                group.id,
                group_name=new_group_name,
                original_group_name=original_group_name,
            ),
            scope=cls.scope(),
        )
        return group

    @classmethod
    def scope(cls) -> ActionScopeStr:
        return RootActionScopeType.value()

    @classmethod
    def undo(
        cls,
        user: AbstractUser,
        params: Params,
        action_to_undo: Action,
    ):
        group = CoreHandler().get_group_for_update(params.group_id)
        CoreHandler().update_group(
            user,
            group,
            name=params.original_group_name,
        )

    @classmethod
    def redo(
        cls,
        user: AbstractUser,
        params: Params,
        action_to_redo: Action,
    ):
        group = CoreHandler().get_group_for_update(params.group_id)
        CoreHandler().update_group(
            user,
            group,
            name=params.group_name,
        )

    @classmethod
    def get_action_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _(
            'Group (%(group_id)s) name changed from "%(original_group_name)s" to "%(group_name)s"'
        ) % {
            "group_id": params.group_id,
            "group_name": params.group_name,
            "original_group_name": params.original_group_name,
        }

    @classmethod
    def get_type_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _("Group updated")


class OrderGroupsActionType(UndoRedoActionType):
    type = "order_groups"

    @dataclasses.dataclass
    class Params:
        group_ids: List[int]
        original_group_ids: List[int]

    @classmethod
    def do(cls, user: AbstractUser, group_ids: List[int]) -> None:
        """
        Changes the order of groups for a user.
        See baserow.core.handler.CoreHandler.order_groups for more details. Undoing
        this action restores the original order of groups prior to this action being
        performed, redoing this restores the new order set initially.

        :param user: The user ordering the groups.
        :param group_ids: The ids of the groups to order.
        """

        original_group_ids = CoreHandler().get_groups_order(user)

        CoreHandler().order_groups(user, group_ids)

        cls.register_action(
            user=user,
            params=cls.Params(
                group_ids,
                original_group_ids,
            ),
            scope=cls.scope(),
        )

    @classmethod
    def scope(cls) -> ActionScopeStr:
        return RootActionScopeType.value()

    @classmethod
    def undo(
        cls,
        user: AbstractUser,
        params: Params,
        action_to_undo: Action,
    ):
        CoreHandler().order_groups(user, params.original_group_ids)

    @classmethod
    def redo(
        cls,
        user: AbstractUser,
        params: Params,
        action_to_redo: Action,
    ):
        CoreHandler().order_groups(user, params.group_ids)

    @classmethod
    def get_action_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _("Groups order changed")

    @classmethod
    def get_type_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _("Groups reordered")


class OrderApplicationsActionType(UndoRedoActionType):
    type = "order_applications"

    @dataclasses.dataclass
    class Params:
        group_id: int
        group_name: str
        application_ids: List[int]
        original_application_ids: List[int]

    @classmethod
    def do(cls, user: AbstractUser, group: Group, application_ids: List[int]) -> Any:
        """
        Reorders the applications of a given group in the desired order. The index of
        the id in the list will be the new order. See
        `baserow.core.handler.CoreHandler.order_applications` for further details. When
        undone re-orders the applications back to the old order, when redone reorders
        to the new order.

        :param user: The user on whose behalf the applications are reordered.
        :param group: The group where the applications are in.
        :param application_ids: A list of ids in the new order.
        """

        original_application_ids = list(
            CoreHandler().order_applications(user, group, application_ids)
        )

        params = cls.Params(
            group.id, group.name, application_ids, original_application_ids
        )
        cls.register_action(user, params, cls.scope(group.id))

    @classmethod
    def scope(cls, group_id: int) -> ActionScopeStr:
        return GroupActionScopeType.value(group_id)

    @classmethod
    def undo(cls, user: AbstractUser, params: Params, action_being_undone: Action):
        group = CoreHandler().get_group_for_update(params.group_id)
        CoreHandler().order_applications(user, group, params.original_application_ids)

    @classmethod
    def redo(cls, user: AbstractUser, params: Params, action_being_redone: Action):
        group = CoreHandler().get_group_for_update(params.group_id)
        CoreHandler().order_applications(user, group, params.application_ids)

    @classmethod
    def get_action_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _(
            'Applications order changed in group "%(group_name)s" (%(group_id)s)'
        ) % {"group_id": params.group_id, "group_name": params.group_name}

    @classmethod
    def get_type_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _("Applications reordered")


class CreateApplicationActionType(UndoRedoActionType):
    type = "create_application"

    @dataclasses.dataclass
    class Params:
        group_id: int
        group_name: str
        application_type: str
        application_id: int
        application_name: str

    @classmethod
    def do(
        cls,
        user: AbstractUser,
        group: Group,
        application_type: str,
        name: str,
        init_with_data: bool = False,
    ) -> Any:
        """
        Creates a new application based on the provided type. See
        baserow.core.handler.CoreHandler.create_application for further details.
        Undoing this action trashes the application and redoing restores it.

        :param user: The user creating the application.
        :param group: The group to create the application in.
        :param application_type: The type of application to create.
        :param name: The name of the new application.
        :param init_with_data: Whether the application should be initialized with
            some default data. Defaults to False.
        :return: The created Application model instance.
        """

        application = CoreHandler().create_application(
            user, group, application_type, name=name, init_with_data=init_with_data
        )

        application_type = application_type_registry.get_by_model(
            application.specific_class
        )

        params = cls.Params(
            group.id,
            group.name,
            application_type.type,
            application.id,
            application.name,
        )
        cls.register_action(user, params, cls.scope(group.id))

        return application

    @classmethod
    def scope(cls, group_id: int) -> ActionScopeStr:
        return GroupActionScopeType.value(group_id)

    @classmethod
    def undo(cls, user: AbstractUser, params: Params, action_being_undone: Action):
        application = Application.objects.get(id=params.application_id)
        CoreHandler().delete_application(user, application)

    @classmethod
    def redo(cls, user: AbstractUser, params: Params, action_being_redone: Action):
        TrashHandler.restore_item(
            user, "application", params.application_id, parent_trash_item_id=None
        )

    @classmethod
    def get_action_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _(
            '%(application_type)s "%(application_name)s" (%(application_id)s) '
            'created in group "%(group_name)s" (%(group_id)s)'
        ) % {
            "application_type": params.application_type.capitalize(),
            "application_name": params.application_name,
            "application_id": params.application_id,
            "group_name": params.group_name,
            "group_id": params.group_id,
        }

    @classmethod
    def get_type_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _("Application created")


class DeleteApplicationActionType(UndoRedoActionType):
    type = "delete_application"

    @dataclasses.dataclass
    class Params:
        group_id: int
        group_name: str
        application_type: str
        application_id: int
        application_name: str

    @classmethod
    def do(cls, user: AbstractUser, application: Application) -> None:
        """
        Deletes an existing application instance if the user has access to the
        related group. The `application_deleted` signal is also called.
        See baserow.core.handler.CoreHandler.delete_application for further details.
        Undoing this action restores the application and redoing trashes it.

        :param user: The user on whose behalf the application is deleted.
        :param application: The application instance that needs to be deleted.
        """

        CoreHandler().delete_application(user, application)

        group = application.group
        application_type = application_type_registry.get_by_model(
            application.specific_class
        )
        params = cls.Params(
            group.id,
            group.name,
            application_type.type,
            application.id,
            application.name,
        )
        cls.register_action(user, params, cls.scope(application.group.id))

    @classmethod
    def scope(cls, group_id: int) -> ActionScopeStr:
        return GroupActionScopeType.value(group_id)

    @classmethod
    def undo(cls, user, params: Params, action_being_undone: Action):
        TrashHandler.restore_item(
            user, "application", params.application_id, parent_trash_item_id=None
        )

    @classmethod
    def redo(cls, user: AbstractUser, params: Params, action_being_redone: Action):
        application = CoreHandler().get_application(params.application_id)
        CoreHandler().delete_application(user, application)

    @classmethod
    def get_action_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _(
            '%(application_type)s "%(application_name)s" (%(application_id)s) '
            'moved into trash in group "%(group_name)s" (%(group_id)s)'
        ) % {
            "application_type": params.application_type.capitalize(),
            "application_name": params.application_name,
            "application_id": params.application_id,
            "group_name": params.group_name,
            "group_id": params.group_id,
        }

    @classmethod
    def get_type_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _("Application deleted")


class UpdateApplicationActionType(UndoRedoActionType):
    type = "update_application"

    @dataclasses.dataclass
    class Params:
        group_id: int
        group_name: str
        application_type: str
        application_id: int
        application_name: str
        original_application_name: str

    @classmethod
    def do(cls, user: AbstractUser, application: Application, name: str) -> Application:
        """
        Updates an existing application instance.
        See baserow.core.handler.CoreHandler.update_application for further details.
        Undoing this action restore the original_name while redoing set name again.

        :param user: The user on whose behalf the application is updated.
        :param application: The application instance that needs to be updated.
        :param name: The new name of the application.
        :raises ValueError: If one of the provided parameters is invalid.
        :return: The updated application instance.
        """

        original_name = application.name

        application = CoreHandler().update_application(user, application, name)
        application_type = application_type_registry.get_by_model(
            application.specific_class
        )
        group = application.group

        params = cls.Params(
            group.id,
            group.name,
            application_type.type,
            application.id,
            name,
            original_name,
        )
        cls.register_action(user, params, cls.scope(application.group.id))

        return application

    @classmethod
    def scope(cls, group_id: int) -> ActionScopeStr:
        return GroupActionScopeType.value(group_id)

    @classmethod
    def undo(cls, user: AbstractUser, params: Params, action_being_undone: Action):
        application = CoreHandler().get_application(params.application_id)
        CoreHandler().update_application(
            user, application, params.original_application_name
        )

    @classmethod
    def redo(cls, user: AbstractUser, params: Params, action_being_redone: Action):
        application = CoreHandler().get_application(params.application_id)
        CoreHandler().update_application(user, application, params.application_name)

    @classmethod
    def get_action_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _(
            '%(application_type)s %(application_id)s renamed from "%(original_name)s" '
            'to "%(application_name)s" in group "%(group_name)s" (%(group_id)s)'
        ) % {
            "group_id": params.group_id,
            "group_name": params.group_name,
            "application_type": params.application_type,
            "application_name": params.application_name,
            "application_id": params.application_id,
            "original_name": params.original_application_name,
        }

    @classmethod
    def get_type_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _("Application updated")


class DuplicateApplicationActionType(UndoRedoActionType):
    type = "duplicate_application"

    @dataclasses.dataclass
    class Params:
        group_id: int
        group_name: str
        application_type: str
        application_id: int
        application_name: str
        original_application_id: int
        original_application_name: str

    @classmethod
    def do(
        cls,
        user: AbstractUser,
        application: Application,
        progress_builder: Optional[ChildProgressBuilder] = None,
    ) -> Application:
        """
        Duplicate an existing application instance.
        See baserow.core.handler.CoreHandler.duplicate_application for further details.
        Undoing this action trashes the application and redoing restores it.

        :param user: The user on whose behalf the application is duplicated.
        :param application: The application instance that needs to be duplicated.
        :param progress_builder: A progress builder instance that can be used to
            track the progress of the duplication.
        :return: The new (duplicated) application instance.
        """

        new_app_clone = CoreHandler().duplicate_application(
            user,
            application,
            progress_builder,
        )
        application_type = application_type_registry.get_by_model(
            application.specific_class
        )
        group = application.group

        params = cls.Params(
            group.id,
            group.name,
            application_type.type,
            new_app_clone.id,
            new_app_clone.name,
            application.id,
            application.name,
        )
        cls.register_action(user, params, cls.scope(application.group.id))

        return new_app_clone

    @classmethod
    def scope(cls, group_id: int) -> ActionScopeStr:
        return GroupActionScopeType.value(group_id)

    @classmethod
    def undo(cls, user: AbstractUser, params: Params, action_being_undone: Action):
        application = CoreHandler().get_application(params.application_id)
        CoreHandler().delete_application(user, application)

    @classmethod
    def redo(cls, user: AbstractUser, params: Params, action_being_redone: Action):
        TrashHandler.restore_item(
            user, "application", params.application_id, parent_trash_item_id=None
        )

    @classmethod
    def get_action_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _(
            '%(application_type)s "%(application_name)s" (%(application_id)s) '
            'created as duplicate from "%(original_app_id)s" (%(original_app_id)s) '
            'in group "%(group_name)s" (%(group_id)s)'
        ) % {
            "group_id": params.group_id,
            "group_name": params.group_name,
            "application_type": params.application_type,
            "application_name": params.application_name,
            "application_id": params.application_id,
            "original_app_id": params.original_application_id,
            "original_app_name": params.original_application_name,
        }

    @classmethod
    def get_type_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _("Application duplicated")


class InstallTemplateActionType(UndoRedoActionType):
    type = "install_template"

    @dataclasses.dataclass
    class Params:
        group_id: int
        group_name: str
        template_id: int
        template_name: str
        installed_applications_ids: List[int]

    @classmethod
    def do(
        cls,
        user: AbstractUser,
        group: Group,
        template: Template,
        progress_builder: Optional[ChildProgressBuilder] = None,
    ) -> List[Application]:
        """
        Install a template into the provided group. See
        baserow.core.handler.CoreHandler.install_template for further details.
        Undoing this action trash the installed applications and redoing
        restore them all.

        :param user: The user on whose behalf the template is installed.
        :param group: The group where the applications will be installed.
        :param template: The template to install.
        :param progress_builder: A progress builder instance that can be used to
            track the progress of the installation.
        :return: The list of installed applications.
        """

        installed_applications, _ = CoreHandler().install_template(
            user,
            group,
            template,
            progress_builder=progress_builder,
        )

        params = cls.Params(
            group.id,
            group.name,
            template.id,
            template.name,
            [app.id for app in installed_applications],
        )
        cls.register_action(user, params, cls.scope(group.id))

        return installed_applications

    @classmethod
    def scope(cls, group_id: int) -> ActionScopeStr:
        return GroupActionScopeType.value(group_id)

    @classmethod
    def undo(cls, user: AbstractUser, params: Params, action_being_undone: Action):
        handler = CoreHandler()
        for application_id in params.installed_applications_ids:
            application = CoreHandler().get_application(application_id)
            handler.delete_application(user, application)

    @classmethod
    def redo(cls, user: AbstractUser, params: Params, action_being_redone: Action):
        for application_id in params.installed_applications_ids:
            TrashHandler.restore_item(
                user, "application", application_id, parent_trash_item_id=None
            )

    @classmethod
    def get_action_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _(
            'Template "%(template_name)s" (%(template_id)s) '
            'installed in group "%(group_name)s" (%(group_id)s)'
        ) % {
            "group_id": params.group_id,
            "group_name": params.group_name,
            "template_name": params.template_name,
            "template_id": params.template_id,
        }

    @classmethod
    def get_type_description(
        cls, user: AbstractUser, params: Params, *args, **kwargs
    ) -> str:
        return _("Template installed")
