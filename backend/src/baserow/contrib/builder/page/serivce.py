from typing import Dict, List

from django.contrib.auth.models import AbstractUser

from baserow.contrib.builder.models import Builder
from baserow.contrib.builder.operations import OrderPagesBuilderOperationType
from baserow.contrib.builder.page.handler import PageHandler
from baserow.contrib.builder.page.models import Page
from baserow.contrib.builder.page.operations import (
    CreatePageOperationType,
    DeletePageOperationType,
    ReadPageOperationType,
    UpdatePageOperationType,
)
from baserow.contrib.builder.page.signals import (
    page_created,
    page_deleted,
    page_updated,
    pages_reordered,
)
from baserow.core.handler import CoreHandler
from baserow.core.utils import extract_allowed


class PageService:
    def __init__(self):
        self.handler = PageHandler()

    def get_page(self, user: AbstractUser, page_id: int):
        page = self.handler.get_page(page_id)

        CoreHandler().check_permissions(
            user,
            ReadPageOperationType.type,
            group=page.builder.group,
            context=page,
        )

        return page

    def create_page(self, user: AbstractUser, builder: Builder, name: str) -> Page:
        CoreHandler().check_permissions(
            user,
            CreatePageOperationType.type,
            group=builder.group,
            context=builder,
        )

        page = self.handler.create_page(builder, name)

        page_created.send(self, page=page, user=user)

        return page

    def delete_page(self, user: AbstractUser, page: Page):
        CoreHandler().check_permissions(
            user,
            DeletePageOperationType.type,
            group=page.builder.group,
            context=page,
        )

        self.handler.delete_page(page)

        page_deleted.send(self, builder=page.builder, page_id=page.id, user=user)

    def update_page(self, user: AbstractUser, page: Page, values: Dict):
        CoreHandler().check_permissions(
            user,
            UpdatePageOperationType.type,
            group=page.builder.group,
            context=page,
        )

        allowed_updates = extract_allowed(values, ["name"])

        self.handler.update_page(page, allowed_updates)

        page_updated.send(self, page=page, user=user)

        return page

    def order_pages(self, user: AbstractUser, builder: Builder, order: List[int]):
        CoreHandler().check_permissions(
            user,
            OrderPagesBuilderOperationType.type,
            group=builder.group,
            context=builder,
        )

        all_pages = Page.objects.filter(builder_id=builder.id)
        user_pages = CoreHandler().filter_queryset(
            user,
            OrderPagesBuilderOperationType.type,
            all_pages,
            group=builder.group,
            context=builder,
        )

        full_order = self.handler.order_pages(builder, order, user_pages)

        pages_reordered.send(self, builder=builder, order=full_order, user=user)

        return full_order
