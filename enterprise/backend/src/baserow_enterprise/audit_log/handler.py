from typing import Any, Dict
from baserow.core.action.models import Action

from .models import AuditLogEntry


class AuditLogHandler:
    @classmethod
    def log_action(cls, action: Action):
        """
        Creates a new audit log entry for the given user, group and event type. The
        kwargs will be stored as JSON in the data field of the audit log entry.

        :param action: The action that should be logged.
        """

        group_id, group_name = None, None
        if hasattr(action.params, "group_id") and hasattr(action.params, "group_name"):
            group_id = action.params.group_id
            group_name = action.params.group_name

        AuditLogEntry.objects.create(
            user_id=action.user.id,
            user_email=action.user.email,
            group_id=group_id,
            group_name=group_name,
            action_id=action.id,
            action_type=action.type,
            action_params=action.params,
            timestamp=action.created_on,
        )
