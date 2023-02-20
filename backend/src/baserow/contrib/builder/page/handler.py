from typing import Dict, List

from baserow.contrib.builder.models import Builder
from baserow.contrib.builder.page.exceptions import PageDoesNotExist, PageNotInBuilder
from baserow.contrib.builder.page.models import Page


class PageHandler:
    def get_page(self, page_id: int):
        try:
            return Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            raise PageDoesNotExist()

    def create_page(self, builder: Builder, name: str) -> Page:
        last_order = Page.get_last_order(builder)
        page = Page.objects.create(builder=builder, name=name, order=last_order)

        return page

    def delete_page(self, page: Page):
        page.delete()

    def update_page(self, page: Page, values: Dict):
        for key, value in values.items():
            setattr(page, key, value)

        page.save()

        return page

    def order_pages(self, builder: Builder, order: List[int], base_qs=None):
        if base_qs is None:
            base_qs = Page.objects.filter(builder=builder)

        page_ids = base_qs.values_list("id", flat=True)

        for page_id in order:
            if page_id not in page_ids:
                raise PageNotInBuilder(page_id)

        full_order = Page.order_objects(base_qs, order)

        return full_order
