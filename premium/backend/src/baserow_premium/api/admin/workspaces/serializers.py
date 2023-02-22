from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from baserow.core.models import Workspace, WorkspaceUser

User = get_user_model()


class WorkspaceAdminUsersSerializer(ModelSerializer):
    id = serializers.IntegerField(source="user.id")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = WorkspaceUser

        fields = ("id", "email", "permissions")


class WorkspacesAdminResponseSerializer(ModelSerializer):
    users = WorkspaceAdminUsersSerializer(source="workspaceuser_set", many=True)
    application_count = serializers.IntegerField()

    class Meta:
        model = Workspace
        fields = (
            "id",
            "name",
            "users",
            "application_count",
            "created_on",
        )
