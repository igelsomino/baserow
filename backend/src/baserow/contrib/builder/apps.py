from django.apps import AppConfig

from baserow.core.registries import object_scope_type_registry, operation_type_registry


class BuilderConfig(AppConfig):
    name = "baserow.contrib.builder"

    def ready(self):
        from baserow.core.registries import application_type_registry

        from .application_types import BuilderApplicationType

        application_type_registry.register(BuilderApplicationType())

        from baserow.contrib.builder.object_scopes import BuilderObjectScopeType

        object_scope_type_registry.register(BuilderObjectScopeType())

        from baserow.contrib.builder.page.operations import CreatePageOperationType

        operation_type_registry.register(CreatePageOperationType())
