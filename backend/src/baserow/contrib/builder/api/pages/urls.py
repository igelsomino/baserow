from django.urls import re_path

from baserow.contrib.builder.api.pages.views import PagesView, PageView

app_name = "baserow.contrib.builder.api.pages"

urlpatterns = [
    re_path(
        r"$",
        PagesView.as_view(),
        name="list",
    ),
    re_path(r"(?P<page_id>[0-9]+)/$", PageView.as_view(), name="item"),
]
