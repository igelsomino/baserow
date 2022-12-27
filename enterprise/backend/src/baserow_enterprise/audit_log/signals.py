from django.dispatch import receiver

from baserow.core.action.signals import action_done


@receiver(action_done)
def register_action_types(sender, **kwargs):
    print("action_registered signal received ", sender, kwargs)
