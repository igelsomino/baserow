from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.db.transaction import Atomic
from django.utils import translation
from django.utils.translation import gettext as _

from baserow.contrib.builder.api.serializers import BuilderSerializer
from baserow.contrib.builder.models import Builder
from baserow.contrib.builder.page.handler import PageHandler
from baserow.core.models import Application
from baserow.core.registries import ApplicationType


class BuilderApplicationType(ApplicationType):
    type = "builder"
    model_class = Builder
    instance_serializer_class = BuilderSerializer

    def get_api_urls(self):
        from .api import urls as api_urls

        return api_urls.urlpatterns

    def export_safe_transaction_context(self, application: Application) -> Atomic:
        return transaction.atomic()

    def init_application(self, user: AbstractUser, application: Application) -> None:
        with translation.override(user.profile.language):
            first_page_name = _("Page")

        PageHandler().create_page(user, application.specific, first_page_name)
