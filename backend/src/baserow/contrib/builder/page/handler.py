from django.contrib.auth.models import AbstractUser

from baserow.contrib.builder.models import Builder
from baserow.contrib.builder.page.model import Page
from baserow.contrib.builder.page.operations import CreatePageOperationType
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
        return Page.objects.create(builder=builder, name=name, order=last_order)
