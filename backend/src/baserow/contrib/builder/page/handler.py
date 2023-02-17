from typing import Dict, List

from django.contrib.auth.models import AbstractUser

from baserow.contrib.builder.models import Builder
from baserow.contrib.builder.operations import OrderPagesBuilderOperationType
from baserow.contrib.builder.page.exceptions import PageDoesNotExist, PageNotInBuilder
from baserow.contrib.builder.page.model import Page
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


class PageHandler:
    def get_page(self, user: AbstractUser, page_id: int):
        try:
            page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            raise PageDoesNotExist()

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

        last_order = Page.get_last_order(builder)
        page = Page.objects.create(builder=builder, name=name, order=last_order)

        page_created.send(self, page=page, user=user)

        return page

    def delete_page(self, user: AbstractUser, page: Page):
        CoreHandler().check_permissions(
            user,
            DeletePageOperationType.type,
            group=page.builder.group,
            context=page,
        )

        page.delete()

        page_deleted.send(self, builder=page.builder, page_id=page.id, user=user)

    def update_page(self, user: AbstractUser, page: Page, values: Dict):
        CoreHandler().check_permissions(
            user,
            UpdatePageOperationType.type,
            group=page.builder.group,
            context=page,
        )

        allowed_updates = extract_allowed(values, ["name"])

        for key, value in allowed_updates.items():
            setattr(page, key, value)

        page.save()

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

        page_ids = user_pages.values_list("id", flat=True)

        for page_id in order:
            if page_id not in page_ids:
                raise PageNotInBuilder(page_id)

        full_order = Page.order_objects(all_pages, order)
        pages_reordered.send(self, builder=builder, order=full_order, user=user)
