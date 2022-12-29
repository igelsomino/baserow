from django.dispatch import receiver

from baserow.core.action.signals import action_done, actions_redone, actions_undone

from .handler import AuditLogHandler


@receiver(action_done)
def log_action(sender, action, action_type, group, **kwargs):
    AuditLogHandler.log_action(action, action_type, group, **kwargs)


@receiver(actions_undone)
def mark_actions_undone(sender, actions, **kwargs):
    AuditLogHandler.mark_actions_undone(actions)


@receiver(actions_redone)
def mark_action_redone(sender, actions, **kwargs):
    AuditLogHandler.mark_actions_redone(actions)
