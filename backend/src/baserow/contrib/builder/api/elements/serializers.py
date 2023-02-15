from django.utils.functional import lazy

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.elements.registries import element_type_registry


class ElementSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(help_text="The type of the element.")

    @extend_schema_field(OpenApiTypes.STR)
    def get_type(self, instance):
        return element_type_registry.get_by_model(instance.specific_class).type

    class Meta:
        model = Element
        fields = ("id", "page_id", "type", "order", "config")
        extra_kwargs = {
            "id": {"read_only": True},
            "page_id": {"read_only": True},
            "type": {"read_only": True},
            "order": {"read_only": True, "help_text": "Lowest first."},
        }


class CreateElementSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=lazy(element_type_registry.get_types, list)(), required=True
    )
    before_id = serializers.IntegerField()

    class Meta:
        model = Element
        fields = ("type", "config", "before_id")
        extra_kwargs = {
            "before_id": {
                "required": False,
                "help_text": "If provided, creates the element before the element "
                "with the given id.",
            },
        }


class UpdateElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ("config",)
        extra_kwargs = {
            "config": {"required": False},
        }


class OrderElementsSerializer(serializers.Serializer):
    elements_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="The ids of the elements in the order they are supposed to be set in",
    )
