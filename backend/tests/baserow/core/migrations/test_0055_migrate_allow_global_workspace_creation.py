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
def test_0055_migrate_allow_global_workspace_creation_forward():
    migrate_from = [
        ("core", "0054_settings_allow_global_workspace_creation"),
    ]
    migrate_to = [
        ("core", "0055_migrate_allow_global_workspace_creation"),
    ]

    old_state = migrate(migrate_from)
    Settings = old_state.apps.get_model("core", "Settings")

    # Turn global group creation off.
    settings, _ = Settings.objects.update_or_create(
        defaults={"allow_global_group_creation": False}
    )

    assert settings.allow_global_group_creation is False
    assert settings.allow_global_workspace_creation is True

    new_state = migrate(migrate_to)
    Settings = new_state.apps.get_model("core", "Settings")

    settings = Settings.objects.all()[:1].get()
    assert settings.allow_global_group_creation is False
    assert settings.allow_global_workspace_creation is False


@pytest.mark.django_db
def test_0055_migrate_allow_global_workspace_creation_backward():
    migrate_from = [
        ("core", "0055_migrate_allow_global_workspace_creation"),
    ]
    migrate_to = [
        ("core", "0054_settings_allow_global_workspace_creation"),
    ]

    old_state = migrate(migrate_from)
    Settings = old_state.apps.get_model("core", "Settings")

    # Turn global workspace creation off.
    settings, _ = Settings.objects.update_or_create(
        defaults={"allow_global_workspace_creation": False}
    )

    assert settings.allow_global_workspace_creation is False
    assert settings.allow_global_group_creation is True

    new_state = migrate(migrate_to)
    Settings = new_state.apps.get_model("core", "Settings")

    settings = Settings.objects.all()[:1].get()
    assert settings.allow_global_workspace_creation is False
    assert settings.allow_global_group_creation is False
