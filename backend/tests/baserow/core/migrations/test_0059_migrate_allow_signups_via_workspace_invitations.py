from django.db import connection
from django.db.migrations.executor import MigrationExecutor

import pytest


def migrate(target):
    executor = MigrationExecutor(connection)
    executor.loader.build_graph()  # reload.
    executor.migrate(target)
    new_state = executor.loader.project_state(target)
    return new_state


@pytest.mark.django_db
def test_0059_migrate_allow_signups_via_workspace_invitations_forward():
    migrate_from = [
        ("core", "0058_settings_allow_signups_via_workspace_invitations"),
    ]
    migrate_to = [
        ("core", "0059_migrate_allow_signups_via_workspace_invitations"),
    ]

    old_state = migrate(migrate_from)
    Settings = old_state.apps.get_model("core", "Settings")

    # Turn signups via group invitations off.
    settings, _ = Settings.objects.update_or_create(
        defaults={"allow_signups_via_group_invitations": False}
    )

    assert settings.allow_signups_via_group_invitations is False
    assert settings.allow_signups_via_workspace_invitations is True

    new_state = migrate(migrate_to)
    Settings = new_state.apps.get_model("core", "Settings")

    settings = Settings.objects.all()[:1].get()
    assert settings.allow_signups_via_group_invitations is False
    assert settings.allow_signups_via_workspace_invitations is False


@pytest.mark.django_db
def test_0059_migrate_allow_signups_via_workspace_invitations_backward():
    migrate_from = [
        ("core", "0059_migrate_allow_signups_via_workspace_invitations"),
    ]
    migrate_to = [
        ("core", "0058_settings_allow_signups_via_workspace_invitations"),
    ]

    old_state = migrate(migrate_from)
    Settings = old_state.apps.get_model("core", "Settings")

    # Turn signups via workspace invitations off.
    settings, _ = Settings.objects.update_or_create(
        defaults={"allow_signups_via_workspace_invitations": False}
    )

    assert settings.allow_signups_via_workspace_invitations is False
    assert settings.allow_signups_via_group_invitations is True

    new_state = migrate(migrate_to)
    Settings = new_state.apps.get_model("core", "Settings")

    settings = Settings.objects.all()[:1].get()
    assert settings.allow_signups_via_workspace_invitations is False
    assert settings.allow_signups_via_group_invitations is False
