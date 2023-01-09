from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from baserow.core.exceptions import PermissionDenied

from baserow_premium.license.features import PREMIUM
from baserow_premium.license.handler import LicenseHandler

from baserow.contrib.database.fields import signals as field_signals
from baserow.contrib.database.fields.models import FileField
from baserow.contrib.database.views import signals as view_signals
from baserow.contrib.database.views.models import OWNERSHIP_TYPE_COLLABORATIVE
from baserow.core.models import Group

from .models import KanbanView


@receiver(field_signals.field_deleted)
def field_deleted(sender, field, **kwargs):
    if isinstance(field, FileField):
        KanbanView.objects.filter(card_cover_image_field_id=field.id).update(
            card_cover_image_field_id=None
        )


def premium_check_ownership_type(
    user: AbstractUser, group: Group, ownership_type: str
) -> None:
    """
    Checks whether the provided ownership type is supported for the user.

    Should be replaced with a support for creating views
    in the ViewOwnershipPermissionManagerType once it is possible.

    :param user: The user on whose behalf the operation is performed.
    :param group: The group for which the check is performed.
    :param ownership_type: View's ownership type.
    :raises PermissionDenied: When not allowed.
    """

    premium = LicenseHandler.user_has_feature(PREMIUM, user, group)

    if premium:
        if ownership_type not in [OWNERSHIP_TYPE_COLLABORATIVE, "personal"]:
            raise PermissionDenied()
    else:
        if ownership_type != OWNERSHIP_TYPE_COLLABORATIVE:
            raise PermissionDenied()


@receiver(view_signals.view_created)
def view_created(sender, view, user, **kwargs):
    group = view.table.database.group
    premium_check_ownership_type(user, group, view.ownership_type)


@receiver(view_signals.views_reordered)
def views_reordered(sender, table, order, ownership_type, user, **kwargs):
    group = table.database.group
    premium_check_ownership_type(user, group, ownership_type)


__all__ = [
    "field_deleted",
    "view_created",
]
