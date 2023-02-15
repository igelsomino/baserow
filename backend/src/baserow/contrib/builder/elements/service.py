from typing import Any, Dict, List

from django.contrib.auth.models import AbstractUser

from baserow.contrib.builder.elements.exceptions import ElementNotInPage
from baserow.contrib.builder.elements.handler import ElementHandler
from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.elements.operations import (
    CreateElementOperationType,
    DeleteElementOperationType,
    ListElementsPageOperationType,
    OrderElementsPageOperationType,
    ReadElementOperationType,
    UpdateElementOperationType,
)
from baserow.contrib.builder.elements.registries import ElementType
from baserow.contrib.builder.elements.signals import (
    element_created,
    element_deleted,
    element_updated,
    elements_reordered,
)
from baserow.contrib.builder.page.model import Page
from baserow.core.handler import CoreHandler


class ElementService:
    def __init__(self):
        self.handler = ElementHandler()

    def get_element(self, user: AbstractUser, element_id: int):

        element = self.handler.get_element(element_id)

        CoreHandler().check_permissions(
            user,
            ReadElementOperationType.type,
            group=element.page.builder.group,
            context=element,
        )

        return element

    def get_elements(self, user: AbstractUser, page: Page):

        CoreHandler().check_permissions(
            user,
            ListElementsPageOperationType.type,
            group=page.builder.group,
            context=page,
        )

        all_elements = self.handler.get_elements(page)

        user_elements = CoreHandler().filter_queryset(
            user,
            ListElementsPageOperationType.type,
            all_elements,
            group=page.builder.group,
            context=page,
        )

        return user_elements

    def create_element(
        self, user: AbstractUser, element_type: ElementType, page: Page, **kwargs
    ) -> Element:
        CoreHandler().check_permissions(
            user,
            CreateElementOperationType.type,
            group=page.builder.group,
            context=page,
        )

        element = self.handler.create_element(element_type, page, **kwargs)

        element_created.send(self, element=element, user=user)

        return element

    def delete_element(self, user: AbstractUser, element: Element):
        CoreHandler().check_permissions(
            user,
            DeleteElementOperationType.type,
            group=element.page.builder.group,
            context=element,
        )

        self.handler.delete_element(element)

        element_deleted.send(self, element_id=element.id)

    def update_element(
        self, user: AbstractUser, element: Element, values: Dict[str, Any]
    ):
        CoreHandler().check_permissions(
            user,
            UpdateElementOperationType.type,
            group=element.page.builder.group,
            context=element,
        )

        element = self.handler.update_element(element, values)

        element_updated.send(self, element=element)

        return element

    def order_elements(self, user: AbstractUser, page: Page, newOrder: List[int]):
        CoreHandler().check_permissions(
            user,
            OrderElementsPageOperationType.type,
            group=page.builder.group,
            context=page,
        )

        all_elements = Element.objects.filter(page=page)

        user_elements = CoreHandler().filter_queryset(
            user,
            OrderElementsPageOperationType.type,
            all_elements,
            group=page.builder.group,
            context=page,
        )

        element_ids = set(user_elements.values_list("id", flat=True))

        # Check if all ids belongs to the page and if the user has access to it
        for element_id in newOrder:
            if element_id not in element_ids:
                raise ElementNotInPage(element_id)

        full_order = self.handler.order_elements(page, newOrder)

        elements_reordered.send(self, page=page, order=full_order, user=user)
