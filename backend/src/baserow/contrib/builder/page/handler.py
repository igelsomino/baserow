from django.contrib.auth.models import AbstractUser

from baserow.contrib.builder.models import Builder
from baserow.contrib.builder.page.model import Page
from baserow.contrib.builder.page.operations import (
    CreatePageOperationType,
    DeletePageOperationType,
)
from baserow.contrib.builder.page.signals import page_created, page_deleted
from baserow.core.handler import CoreHandler


class PageHandler:
    def create_page(self, user: AbstractUser, builder: Builder, name: str) -> Page:
        CoreHandler().check_permissions(
            user,
            CreatePageOperationType.type,
            group=builder.group,
            context=builder,
        )

        last_order = Page.get_last_order(builder)
        page = Page.objects.create(builder=builder, name=name, order=last_order)

        page_created.send(self, page=page, user=user)

        return page

    def delete_page(self, user: AbstractUser, page: Page):
        CoreHandler().check_permissions(
            user,
            DeletePageOperationType.type,
            group=page.builder.group,
            context=page.builder,
        )

        page.delete()

        page_deleted.send(self, page_id=page.id)
