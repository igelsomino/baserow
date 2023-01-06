from typing import TYPE_CHECKING, Any, Optional

from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet

from baserow_premium.license.features import PREMIUM
from baserow_premium.license.handler import LicenseHandler

from baserow.contrib.database.views.models import (
    OWNERSHIP_TYPE_COLLABORATIVE,
    ViewDecoration,
    ViewFilter,
    ViewSort,
)
from baserow.contrib.database.views.operations import (
    CreateViewDecorationOperationType,
    CreateViewFilterOperationType,
    CreateViewSortOperationType,
    DeleteViewDecorationOperationType,
    DeleteViewFilterOperationType,
    DeleteViewOperationType,
    DeleteViewSortOperationType,
    DuplicateViewOperationType,
    ListAggregationViewOperationType,
    ListViewDecorationOperationType,
    ListViewFilterOperationType,
    ListViewsOperationType,
    ListViewSortOperationType,
    OrderViewsOperationType,
    ReadAggregationViewOperationType,
    ReadViewDecorationOperationType,
    ReadViewFieldOptionsOperationType,
    ReadViewFilterOperationType,
    ReadViewOperationType,
    ReadViewsOrderOperationType,
    ReadViewSortOperationType,
    RestoreViewOperationType,
    UpdateViewDecorationOperationType,
    UpdateViewFieldOptionsOperationType,
    UpdateViewFilterOperationType,
    UpdateViewOperationType,
    UpdateViewSlugOperationType,
    UpdateViewSortOperationType,
)
from baserow.core.exceptions import PermissionDenied
from baserow.core.registries import PermissionManagerType

User = get_user_model()


if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser

    from .models import Group


class ViewOwnershipPermissionManagerType(PermissionManagerType):
    type = "view_ownership"
    operations = [
        # views
        # CreateViewOperationType.type is implemented via view_created signal
        #   due to current technical limitations regarding insufficient
        #   context object being passed
        ReadViewOperationType.type,
        UpdateViewOperationType.type,
        UpdateViewSlugOperationType.type,
        DuplicateViewOperationType.type,
        DeleteViewOperationType.type,
        RestoreViewOperationType.type,
        # field options
        ReadViewFieldOptionsOperationType.type,
        UpdateViewFieldOptionsOperationType.type,
        # view filters
        CreateViewFilterOperationType.type,
        ListViewFilterOperationType.type,
        ReadViewFilterOperationType.type,
        UpdateViewFilterOperationType.type,
        DeleteViewFilterOperationType.type,
        # sorts
        CreateViewSortOperationType.type,
        ListViewSortOperationType.type,
        ReadViewSortOperationType.type,
        UpdateViewSortOperationType.type,
        DeleteViewSortOperationType.type,
        # decorations
        CreateViewDecorationOperationType.type,
        ListViewDecorationOperationType.type,
        DeleteViewDecorationOperationType.type,
        UpdateViewDecorationOperationType.type,
        ReadViewDecorationOperationType.type,
        # aggregations
        ListAggregationViewOperationType.type,
        ReadAggregationViewOperationType.type,
        # ordering TODO:
        # "database.table.read_view_order",
        # OrderViewsOperationType.type,
    ]

    def check_permissions(
        self,
        actor: "AbstractUser",
        operation_name: str,
        group: Optional["Group"] = None,
        context: Optional[Any] = None,
        include_trash: bool = False,
    ) -> Optional[bool]:
        """
        check_permissions() impl for view ownership checks.

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

        if not isinstance(actor, User):
            return

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
                return
            if context.ownership_type == "personal" and context.created_by == actor:
                return
            raise PermissionDenied()
        else:
            if context.ownership_type != OWNERSHIP_TYPE_COLLABORATIVE:
                raise PermissionDenied()

        return

    def filter_queryset(
        self,
        actor: "AbstractUser",
        operation_name: str,
        queryset: QuerySet,
        group: Optional["Group"] = None,
        context: Optional[Any] = None,
    ) -> QuerySet:
        """
        filter_queryset() impl for view ownership filtering.

        :param actor: The actor whom we want to filter the queryset for.
            Generally a `User` but can be a Token.
        :param operation: The operation name for which we want to filter the queryset
            for.
        :param group: An optional group into which the operation takes place.
        :param context: An optional context object related to the current operation.
        :return: The queryset potentially filtered.
        """

        if not isinstance(actor, User):
            return queryset

        if operation_name != ListViewsOperationType.type:
            return queryset

        if not group:
            return queryset

        premium = LicenseHandler.user_has_feature(PREMIUM, actor, group)

        if premium:
            return queryset.filter(
                Q(ownership_type=OWNERSHIP_TYPE_COLLABORATIVE)
                | (Q(ownership_type="personal") & Q(created_by=actor))
            )
        else:
            return queryset.filter(ownership_type=OWNERSHIP_TYPE_COLLABORATIVE)
