from django.dispatch import Signal

action_done = Signal()
actions_undone = Signal()
actions_redone = Signal()
