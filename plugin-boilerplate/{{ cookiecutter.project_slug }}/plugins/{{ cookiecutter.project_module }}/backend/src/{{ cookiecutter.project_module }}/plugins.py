import logging
from baserow.core.registries import Plugin
from django.urls import path, include

from .api import urls as api_urls

logger = logging.getLogger(__name__)


class PluginNamePlugin(Plugin):
    type = "{{ cookiecutter.project_module }}"

    def get_api_urls(self):
        return [
            path(
                "{{ cookiecutter.project_module }}/",
                include(api_urls, namespace=self.type),
            ),
        ]
