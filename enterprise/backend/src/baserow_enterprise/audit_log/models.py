from django.db import models
from baserow.core.action.models import JSONEncoderSupportingDataClasses

from baserow.core.action.registries import action_type_registry


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
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    ip_address = models.GenericIPAddressField(null=True)

    def get_type(self):
        try:
            action_type = action_type_registry.get(self.action_type)
        except action_type_registry.does_not_exist_exception_class:
            return self.action_type

        return action_type.get_type_description(
            action_type.Params(**self.action_params)
        )

    def get_description(self):
        try:
            action_type = action_type_registry.get(self.action_type)
        except action_type_registry.does_not_exist_exception_class:
            return f"Unknown action type: {self.action_type} - {self.action_params}"

        return action_type.get_action_description(
            action_type.Params(**self.action_params)
        )

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(
                fields=["user_email", "group_name", "action_type", "timestamp"],
            )
        ]
