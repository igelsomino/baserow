import dataclasses
from typing import Any, List, Optional, Type

from baserow.api.sessions import get_user_remote_addr_ip
from baserow.core.action.models import Action
from baserow.core.action.registries import ActionType
from baserow.core.models import Group

from .models import AuditLogEntry


class AuditLogHandler:
    @classmethod
    def log_action(
        cls,
        action: Action,
        action_type: Type[ActionType],
        group: Optional[Group] = None,
        **kwargs: Any,
    ):
        """
        Creates a new audit log entry for the given user, group and event type. The
        kwargs will be stored as JSON in the data field of the audit log entry.

        :param action: The action that should be logged.
        :param group: The group that the action was performed on.
        """

        group_id, group_name = None, None
        if group is not None:
            group_id = group.id
            group_name = group.name

        type_str, descr_srt = action_type.description
        ip_address = get_user_remote_addr_ip(action.user)

        AuditLogEntry.objects.create(
            user_id=action.user.id,
            user_email=action.user.email,
            group_id=group_id,
            group_name=group_name,
            action_id=action.id,
            action_type=action.type,
            action_params=dataclasses.asdict(action.params),
            timestamp=action.created_on,
            original_type_description=type_str,
            original_action_description=descr_srt,
            ip_address=ip_address,
        )

    @classmethod
    def mark_actions_undone(cls, actions: List[Action]):
        """
        Marks the given actions as undone in the audit log.

        :param actions: The actions that should be marked as undone.
        """

        AuditLogEntry.objects.filter(
            action_id__in=[action.id for action in actions]
        ).update(action_undone_at=actions[0].undone_at)

    @classmethod
    def mark_actions_redone(cls, actions: List[Action]):
        """
        Marks the given actions as redone in the audit log.

        :param actions: The actions that should be marked as redone.
        """

        AuditLogEntry.objects.filter(
            action_id__in=[action.id for action in actions]
        ).update(action_undone_at=None)
