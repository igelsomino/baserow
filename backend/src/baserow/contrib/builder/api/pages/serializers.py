from rest_framework import serializers

from baserow.contrib.builder.page.model import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ("id", "name", "order", "builder_id")
        extra_kwargs = {
            "id": {"read_only": True},
            "builder_id": {"read_only": True},
            "order": {"help_text": "Lowest first."},
        }
