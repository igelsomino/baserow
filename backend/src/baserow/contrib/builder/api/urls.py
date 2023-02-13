from django.urls import include, path

from .pages import urls as page_urls

app_name = "baserow.contrib.builder.api"

urlpatterns = [path("pages/", include(page_urls, namespace="pages"))]
