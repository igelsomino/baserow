from django.contrib.contenttypes.models import ContentType
from django.db import models

from baserow.contrib.builder.page.model import Page
from baserow.core.mixins import (
    CreatedAndUpdatedOnMixin,
    HierarchicalModelMixin,
    OrderableMixin,
    PolymorphicContentTypeMixin,
    TrashableModelMixin,
)


def get_default_element_content_type():
    return ContentType.objects.get_for_model(Element)


class Element(
    HierarchicalModelMixin,
    TrashableModelMixin,
    CreatedAndUpdatedOnMixin,
    OrderableMixin,
    PolymorphicContentTypeMixin,
    models.Model,
):
    """ """

    # uid?
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(help_text="Lowest first.")
    content_type = models.ForeignKey(
        ContentType,
        verbose_name="content type",
        related_name="page_elements",
        on_delete=models.SET(get_default_element_content_type),
    )
    config = models.JSONField(default=dict)
    # style = models.JSONField(default=dict)
    # visibility
    # events->actions

    class Meta:
        ordering = ("order",)

    def get_parent(self):
        return self.page

    @classmethod
    def get_last_order(cls, page):
        queryset = Element.objects.filter(page=page)
        return cls.get_highest_order_of_queryset(queryset) + 1


class HeaderElement(Element):
    pass


class ParagraphElement(Element):
    pass
