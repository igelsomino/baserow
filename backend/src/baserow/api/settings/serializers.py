from rest_framework import serializers

from baserow.core.models import Settings


class SettingsSerializer(serializers.ModelSerializer):
    allow_global_group_creation = serializers.BooleanField(
        required=False,
        source="allow_global_workspace_creation",
        help_text="Indicates whether all users can create groups, or just staff. "
        "Deprecated, please use `allow_global_workspace_creation`.",
    )  # GroupDeprecation
    allow_signups_via_group_invitations = serializers.BooleanField(
        required=False,
        source="allow_signups_via_workspace_invitations",
        help_text="Indicates whether invited users can create an account when signing "
        "up, even if allow_new_signups is disabled. Deprecated, please use "
        "`allow_signups_via_workspace_invitations`.",
    )  # GroupDeprecation

    class Meta:
        model = Settings
        fields = (
            "allow_new_signups",
            "allow_signups_via_workspace_invitations",
            "allow_signups_via_group_invitations",  # GroupDeprecation
            "allow_reset_password",
            "allow_global_workspace_creation",
            "allow_global_group_creation",  # GroupDeprecation
            "account_deletion_grace_delay",
            "show_admin_signup_page",
        )
        extra_kwargs = {
            "allow_new_signups": {"required": False},
            "allow_signups_via_workspace_invitations": {"required": False},
            "allow_reset_password": {"required": False},
            "allow_global_workspace_creation": {"required": False},
            "account_deletion_grace_delay": {"required": False},
        }


class InstanceIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ("instance_id",)
        extra_kwargs = {
            "instance_id": {"read_only": True},
        }
