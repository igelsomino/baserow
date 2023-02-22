from django.http import HttpResponse
from django.urls import include, path

from drf_spectacular.views import SpectacularJSONAPIView, SpectacularRedocView

from baserow.compat.api.groups import urls as group_compat_urls
from baserow.core.registries import application_type_registry, plugin_registry

from .applications import urls as application_urls
from .auth_provider import urls as auth_provider_urls
from .jobs import urls as jobs_urls
from .settings import urls as settings_urls
from .snapshots import urls as snapshots_urls
from .templates import urls as templates_urls
from .trash import urls as trash_urls
from .user import urls as user_urls
from .user_files import urls as user_files_urls
from .workspaces import urls as workspace_urls

app_name = "baserow.api"


def public_health_check(request):
    return HttpResponse("OK")


urlpatterns = (
    [
        path("schema.json", SpectacularJSONAPIView.as_view(), name="json_schema"),
        path(
            "redoc/",
            SpectacularRedocView.as_view(url_name="api:json_schema"),
            name="redoc",
        ),
        path("settings/", include(settings_urls, namespace="settings")),
        path("auth-provider/", include(auth_provider_urls, namespace="auth_provider")),
        path("user/", include(user_urls, namespace="user")),
        path("user-files/", include(user_files_urls, namespace="user_files")),
        path("groups/", include(group_compat_urls, namespace="groups")),
        path("workspaces/", include(workspace_urls, namespace="workspaces")),
        path("templates/", include(templates_urls, namespace="templates")),
        path("applications/", include(application_urls, namespace="applications")),
        path("trash/", include(trash_urls, namespace="trash")),
        path("jobs/", include(jobs_urls, namespace="jobs")),
        path("snapshots/", include(snapshots_urls, namespace="snapshots")),
        path("_health/", public_health_check, name="public_health_check"),
    ]
    + application_type_registry.api_urls
    + plugin_registry.api_urls
)
