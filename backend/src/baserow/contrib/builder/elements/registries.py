from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Type

from rest_framework import serializers

from baserow.core.registry import (
    CustomFieldsInstanceMixin,
    CustomFieldsRegistryMixin,
    ImportExportMixin,
    Instance,
    ModelInstanceMixin,
    ModelRegistryMixin,
    Registry,
)

if TYPE_CHECKING:
    from baserow.contrib.builder.pages.models import Page

from .models import Element


class ElementType(
    CustomFieldsInstanceMixin, ModelInstanceMixin, ImportExportMixin, Instance, ABC
):
    """Element type"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.serializer_field_overrides = {
            "config": self.get_config_serializer_class()(
                required=False,
                help_text="The configuration of the element.",
            ),
        }

    @abstractmethod
    def get_config_serializer_class(self) -> Type[serializers.Serializer]:
        ...

    def export_serialized(
        self,
        element: Element,
    ) -> Dict[str, Any]:
        """
        Exports the field to a serialized dict that can be imported by the
        `import_serialized` method. This dict is also JSON serializable.

        :param element: The element instance that must be serialized.
        :return: The exported field in as serialized dict.
        """

        serialized = {
            "id": element.id,
            "type": self.type,
            "order": element.order,
            "config": element.config,
            # "style": element.style,
        }

        return serialized

    def import_serialized(
        self,
        page: "Page",
        serialized_values: Dict[str, Any],
        id_mapping: Dict[str, Any],
    ) -> Element:
        """ """

        if "builder_elements" not in id_mapping:
            id_mapping["builder_elements"] = {}

        serialized_copy = serialized_values.copy()

        # Remove extra keys
        element_id = serialized_copy.pop("id")
        serialized_copy.pop("type")

        element = self.model_class(page=page, **serialized_copy)
        element.save()

        id_mapping["builder_elements"][element_id] = element.id

        return Element

    @abstractmethod
    def get_sample_params(self) -> Dict[str, Any]:
        ...

    def get_serializer_class(self, *args, **kwargs):
        # Add meta ref name to avoid name collision
        return super().get_serializer_class(
            *args,
            meta_ref_name=f"Generated{self.type.capitalize()}{kwargs['base_class'].__name__}",
            **kwargs,
        )


class ElementTypeRegistry(Registry, ModelRegistryMixin, CustomFieldsRegistryMixin):
    """
    Contains all registered element types.
    """

    name = "element_type"


element_type_registry = ElementTypeRegistry()
