from django.urls import include, path, re_path

from .pages import urls as page_urls

app_name = "baserow.contrib.builder.api"

pages_paths_with_builder_id = [
    path(
        "pages/",
        include(
            page_urls,
            namespace="pages",
        ),
    )
]


urlpatterns = [
    re_path(
        "builder/(?P<builder_id>[0-9]+)/",
        include(
            (pages_paths_with_builder_id, app_name),
            namespace="builder",
        ),
    )
]
