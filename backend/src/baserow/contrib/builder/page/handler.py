from typing import Dict, List

from django.db.models import QuerySet

from baserow.contrib.builder.models import Builder
from baserow.contrib.builder.page.exceptions import PageDoesNotExist, PageNotInBuilder
from baserow.contrib.builder.page.models import Page


class PageHandler:
    def get_page(self, page_id: int, base_queryset: QuerySet = None) -> Page:
        """
        Gets a page by ID

        :param page_id: The ID of the page
        :param base_queryset: Can be provided to already filter or apply performance
            improvements to the queryset when it's being executed
        :raises PageDoesNotExist: If the page doesn't exist
        :return: The model instance of the Page
        """

        if base_queryset is None:
            base_queryset = Page.objects

        try:
            return base_queryset.get(id=page_id)
        except Page.DoesNotExist:
            raise PageDoesNotExist()

    def create_page(self, builder: Builder, name: str) -> Page:
        """
        Creates a new page

        :param builder: The builder the page belongs to
        :param name: The name of the page
        :return: The newly created page instance
        """

        last_order = Page.get_last_order(builder)
        page = Page.objects.create(builder=builder, name=name, order=last_order)

        return page

    def delete_page(self, page: Page):
        """
        Deletes the page provided

        :param page: The page that's supposed to be deleted
        """

        page.delete()

    def update_page(self, page: Page, **kwargs) -> Page:
        """
        Updates fields of a page

        :param page: The page that should be updated
        :param values: The fields that should be updated with their corresponding value
        :return: The updated page
        """

        for key, value in kwargs.items():
            setattr(page, key, value)

        page.save()

        return page

    def order_pages(
        self, builder: Builder, order: List[int], base_qs=None
    ) -> List[int]:
        """
        Assigns a new order to the pages in a builder application.
        You can provide a base_qs for pre-filter the pages affected by this change.

        :param builder: The builder that the pages belong to
        :param order: The new order of the pages
        :param base_qs: A QS that can have filters already applied
        :return: The new order of the pages
        """

        if base_qs is None:
            base_qs = Page.objects.filter(builder=builder)

        page_ids = base_qs.values_list("id", flat=True)

        for page_id in order:
            if page_id not in page_ids:
                raise PageNotInBuilder(page_id)

        full_order = Page.order_objects(base_qs, order)

        return full_order
