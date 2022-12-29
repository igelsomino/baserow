from functools import wraps

from django.db import models
from django.utils.translation import gettext_lazy as _

from baserow.core.action.models import JSONEncoderSupportingDataClasses
from baserow.core.action.registries import action_type_registry


def action_type_getter(fallback_attr: str):
    def decorate_audit_log_entry_attr(func):
        @wraps(func)
        def wrapper(audit_log_entry, *args, **kwargs):
            """
            This wrapper ensure a string is returned even if the action type is not
            registered anymore or if Param class is changed.
            """

            fallback_str = getattr(audit_log_entry, fallback_attr) or ""
            try:
                action_type = action_type_registry.get(audit_log_entry.action_type)
                return func(audit_log_entry, action_type, audit_log_entry.action_params)
            except Exception:
                return _(fallback_str) % audit_log_entry.action_params

        return wrapper

    return decorate_audit_log_entry_attr


class ActionDoneManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(action_undone_at=None)


class AuditLogEntry(models.Model):
    user_id = models.PositiveIntegerField(db_index=True, null=True)
    user_email = models.CharField(max_length=150, db_index=True, null=True, blank=True)

    group_id = models.PositiveIntegerField(db_index=True, null=True)
    group_name = models.CharField(max_length=160, db_index=True, null=True, blank=True)

    action_id = models.PositiveIntegerField(db_index=True, null=True)
    action_type = models.TextField(db_index=True)
    action_params = models.JSONField(
        null=True, encoder=JSONEncoderSupportingDataClasses
    )
    action_undone_at = models.DateTimeField(null=True)

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    # we don't want that a change in the original action type or action description
    # break the audit log. So we store the original description and type in the
    # database so to use it as a fallback just in case.
    original_type_description = models.TextField(null=True, blank=True)
    original_action_description = models.TextField(null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True)

    objects = models.Manager()
    entries = ActionDoneManager()

    @action_type_getter(fallback_attr="original_type_description")
    def get_type(self, action_type, params):
        return action_type.get_type_description(params)

    @action_type_getter(fallback_attr="original_action_description")
    def get_description(self, action_type, params):
        return action_type.get_action_description(params)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(
                fields=[
                    "user_email",
                    "group_name",
                    "action_type",
                    "action_undone_at",
                    "timestamp",
                ],
            )
        ]
