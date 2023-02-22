from django.urls import re_path

from baserow.compat.api.trash.views import TrashContentsCompatView

from .views import TrashContentsView, TrashItemView, TrashStructureView

app_name = "baserow.api.trash"

urlpatterns = [
    re_path(r"^$", TrashStructureView.as_view(), name="list"),
    re_path(
        r"^workspace/(?P<workspace_id>[0-9]+)/$",
        TrashContentsView.as_view(),
        name="contents",
    ),
    re_path(
        r"^restore/$",
        TrashItemView.as_view(),
        name="restore",
    ),
]

# GroupDeprecation
urlpatterns += [
    re_path(
        r"^group/(?P<group_id>[0-9]+)/$",
        TrashContentsCompatView.as_view(),
        name="contents",
    ),
]
