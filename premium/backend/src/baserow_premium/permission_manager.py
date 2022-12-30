from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional
from xmlrpc.client import Boolean # TODO:
from django.db.models import QuerySet, Q

from baserow.core.exceptions import (
    ApplicationTypeAlreadyRegistered,
    ApplicationTypeDoesNotExist,
    AuthenticationProviderTypeAlreadyRegistered,
    AuthenticationProviderTypeDoesNotExist,
    ObjectScopeTypeAlreadyRegistered,
    ObjectScopeTypeDoesNotExist,
    OperationTypeAlreadyRegistered,
    OperationTypeDoesNotExist,
    PermissionDenied,
    PermissionManagerTypeAlreadyRegistered,
    PermissionManagerTypeDoesNotExist,
)
from baserow.core.registries import (
    OperationType,
    PermissionManagerType,
    operation_type_registry,
)
from baserow.contrib.database.table.models import Table
from baserow.contrib.database.views.models import ViewFilter
from baserow.contrib.database.views.operations import (
    CreateViewFilterOperationType,
    CreateViewOperationType,
    CreateViewSortOperationType,
    DeleteViewDecorationOperationType,
    DeleteViewFilterOperationType,
    DeleteViewOperationType,
    DeleteViewSortOperationType,
    DuplicateViewOperationType,
    OrderViewsOperationType,
    ReadViewFilterOperationType,
    ReadViewOperationType,
    ReadViewsOrderOperationType,
    ReadViewSortOperationType,
    UpdateViewFieldOptionsOperationType,
    UpdateViewFilterOperationType,
    UpdateViewOperationType,
    UpdateViewSlugOperationType,
    UpdateViewSortOperationType,
)
from baserow.contrib.database.fields.models import Field
from baserow.contrib.database.views.models import View, ViewSort, ViewDecoration, OWNERSHIP_TYPE_COLLABORATIVE
from baserow_premium.license.handler import LicenseHandler
from baserow_premium.license.features import PREMIUM


if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    from .models import Group


# TODO: bypass public views

class ViewOwnershipPermissionManagerType(PermissionManagerType):
    # TODO: refactor from strings to types?
    type = "view_ownership"
    operations = [
        # views
        # "database.table.create_view", # TODO: ?
        "database.table.view.read",
        "database.table.view.update",
        "database.table.view.update_slug",
        "database.table.view.duplicate",
        "database.table.view.delete",
        "database.table.view.restore",

        # field options
        "database.table.view.read_field_options",
        "database.table.view.update_field_options",

        # view filters
        "database.table.view.create_filter",
        "database.table.view.list_filter",
        "database.table.view.filter.read",
        "database.table.view.filter.update",
        "database.table.view.filter.delete",

        # sorts
        "database.table.view.create_sort",
        "database.table.view.list_sort",
        "database.table.view.sort.read",
        "database.table.view.sort.update",
        "database.table.view.sort.delete",

        # decorations
        "database.table.view.create_decoration",
        "database.table.view.list_decoration",
        "database.table.view.decoration.delete",
        "database.table.view.decoration.update",
        "database.table.view.decoration.read",

        # aggregations
        "database.table.view.list_aggregations",
        # "database.table.field.read_aggregation", # TODO: ?

        # ordering
        # "database.table.read_view_order",
        # "database.table.order_views",
    ]

    def check_permissions(
        self,
        actor: "AbstractUser",
        operation_name: str,
        group: Optional["Group"] = None,
        context: Optional[Any] = None,
        include_trash: Boolean = False,
    ) -> Optional[Boolean]:
        """
        This method is called each time a permission on an operation is checked by the
        `CoreHandler().check_permissions()` method if the current permission manager is
        listed in the `settings.PERMISSION_MANAGERS` list.

        It should:
            - return `True` if the operation is permitted given the other parameters
            - raise a `PermissionDenied` exception if the operation is disallowed
            - return `None` if the condition required by the permission manager are not
              met.

        By default, this method raises a PermissionDenied exception.

        :param actor: The actor who wants to execute the operation. Generally a `User`,
            but can be a `Token`.
        :param operation_name: The operation name the actor wants to execute.
        :param group: The optional group in which  the operation takes place.
        :param context: The optional object affected by the operation. For instance
            if you are updating a `Table` object, the context is this `Table` object.
        :param include_trash: If true then also checks if the given group has been
            trashed instead of raising a DoesNotExist exception.
        :raise PermissionDenied: If the operation is disallowed a PermissionDenied is
            raised.
        :return: `True` if the operation is permitted, None if the permission manager
            can't decide.
        """

        # TODO: remove
        print("*** View Ownership Permission Manager")
        print(operation_name)
        print(context)

        operation_type = operation_type_registry.get(operation_name)

        if operation_name not in self.operations:
            return

        if not group:
            return
        
        if not context:
            return

        premium = LicenseHandler.user_has_feature(PREMIUM, actor, group)

        if isinstance(context, ViewFilter):
            context = context.view

        if isinstance(context, ViewSort):
            context = context.view

        if isinstance(context, ViewDecoration):
            context = context.view

        if premium:
            if context.ownership_type == OWNERSHIP_TYPE_COLLABORATIVE:
                return True
            if context.ownership_type == "personal" and context.created_by == actor:
                return True
            raise PermissionDenied()
        else:
            if context.ownership_type != OWNERSHIP_TYPE_COLLABORATIVE:
                raise PermissionDenied()

        return

    # def get_permissions_object(
    #     self, actor: "AbstractUser", group: Optional["Group"] = None
    # ) -> Any:
    #     """
    #     This method should return the data necessary to easily check a permission from
    #     a client. This object can be used for instance from the frontend to hide or
    #     show UI element accordingly to the user permissions.
    #     The data set returned must contain all the necessary information to prevent and
    #     the client shouldn't have to get more data to decide.

    #     This method is called when the `CoreHandler().get_permissions()` is called,
    #     if the permission manager is listed in the `settings.PERMISSION_MANAGERS`.
    #     It can return `None` if this permission manager is not relevant for the given
    #     actor/group for some reason.

    #     By default this method returns None.

    #     :param actor: The actor whom we want to compute the permission object for.
    #     :param group: The optional group into which we want to compute the permission
    #         object.
    #     :return: The permission object or None.
    #     """

    #     return None

    def filter_queryset(
        self,
        actor: "AbstractUser",
        operation_name: str,
        queryset: QuerySet,
        group: Optional["Group"] = None,
        context: Optional[Any] = None,
    ) -> QuerySet:
        """
        This method allows a permission manager to filter a given queryset accordingly
        to the actor permissions in the specified context. The
        `CoreHandler().filter_queryset()` method calls each permission manager listed in
        `settings.PERMISSION_MANAGERS` to successively filter the given queryset.

        :param actor: The actor whom we want to filter the queryset for.
            Generally a `User` but can be a Token.
        :param operation: The operation name for which we want to filter the queryset
            for.
        :param group: An optional group into which the operation takes place.
        :param context: An optional context object related to the current operation.
        :return: The queryset potentially filtered.
        """

        if operation_name != "database.table.list_views":
            return queryset

        if not group:
            return queryset

        premium = LicenseHandler.user_has_feature(PREMIUM, actor, group)

        if premium:
            return queryset.filter(Q(ownership_type=OWNERSHIP_TYPE_COLLABORATIVE) | (Q(ownership_type="personal") & Q(created_by=actor)))
        else:
            return queryset.filter(ownership_type=OWNERSHIP_TYPE_COLLABORATIVE)
