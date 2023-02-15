from rest_framework import serializers


class HeaderElementConfigSerializer(serializers.Serializer):
    value = serializers.CharField(help_text="The label displayed in the header.")


class ParagraphElementConfigSerializer(serializers.Serializer):
    content = serializers.CharField(help_text="The paragraph content.")
