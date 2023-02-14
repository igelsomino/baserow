from django.urls import re_path

from baserow.contrib.builder.api.pages.views import PageView

app_name = "baserow.contrib.builder.api.pages"

urlpatterns = [
    re_path(
        r"builder/(?P<builder_id>[0-9]+)/$",
        PageView.as_view(),
        name="create",
    ),
]
