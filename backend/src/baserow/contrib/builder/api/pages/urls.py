from django.urls import re_path

from baserow.contrib.builder.api.pages.views import PageView

app_name = "baserow.contrib.builder.api.pages"

urlpatterns = [
    re_path(
        r"/$",
        PageView.as_view(),
        name="create",
    ),
]
