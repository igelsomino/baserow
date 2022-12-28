from django.dispatch import receiver

from baserow.core.action.signals import action_done
from .handler import AuditLogHandler


@receiver(action_done)
def register_action_types(sender, action, **kwargs):
    AuditLogHandler.log_action(action)
