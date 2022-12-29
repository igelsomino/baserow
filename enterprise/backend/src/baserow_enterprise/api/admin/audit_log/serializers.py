from rest_framework import serializers

from baserow_enterprise.audit_log.models import AuditLogEntry


class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_user(self, obj):
        return f"{obj.user_email} ({obj.user_id})"

    def get_group(self, obj):
        if obj.group_id is None:
            return ""
        return f"{obj.group_name} ({obj.group_id})"

    def get_type(self, obj):
        return obj.get_type()

    def get_description(self, obj):
        return obj.get_description()

    class Meta:
        model = AuditLogEntry
        fields = (
            "id",
            "user",
            "group",
            "type",
            "timestamp",
            "description",
            "ip_address",
        )


class AuditLogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLogEntry
        fields = ("user_email",)

    def to_representation(self, instance):
        return {"id": instance.user_email, "value": instance.user_email}


class AuditLogGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLogEntry
        fields = ("group_name",)

    def to_representation(self, instance):
        return {"id": instance.group_name, "value": instance.group_name}


class AuditLogActionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLogEntry
        fields = ("action_type",)

    def to_representation(self, instance):
        return {"id": instance.action_type, "value": instance.get_type()}
