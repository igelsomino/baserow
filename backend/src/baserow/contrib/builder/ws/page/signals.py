from django.db import transaction
from django.dispatch import receiver

from baserow.contrib.builder.api.pages.serializers import PageSerializer
from baserow.contrib.builder.page import signals as page_signals
from baserow.contrib.builder.page.object_scopes import BuilderPageObjectScopeType
from baserow.contrib.builder.page.operations import ReadPageOperationType
from baserow.ws.tasks import broadcast_to_permitted_users


@receiver(page_signals.page_created)
def page_created(sender, page, user, **kwargs):
    transaction.on_commit(
        lambda: broadcast_to_permitted_users.delay(
            page.builder.group_id,
            ReadPageOperationType.type,
            BuilderPageObjectScopeType.type,
            page.id,
            {"type": "page_created", "page": PageSerializer(page).data},
            getattr(user, "web_socket_id", None),
        )
    )
