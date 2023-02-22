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
def test_0053_migrate_group_trash_item_type_forwards():
    # Migrate `TrashEntry.trash_item_type` forwards from "group" to "workspace".
    migrate_from = [
        ("core", "0052_auto_20230130_1118"),
    ]
    migrate_to = [
        ("core", "0053_migrate_group_trash_item_type"),
    ]

    old_state = migrate(migrate_from)

    Workspace = old_state.apps.get_model("core", "Workspace")
    workspace = Workspace.objects.create(name="My workspace")
    TrashEntry = old_state.apps.get_model("core", "TrashEntry")

    TrashEntry.objects.create(
        workspace=workspace, trash_item_id=workspace.id, trash_item_type="group"
    )

    assert TrashEntry.objects.filter(trash_item_type="group").count() == 1
    assert TrashEntry.objects.filter(trash_item_type="workspace").count() == 0

    new_state = migrate(migrate_to)

    TrashEntry = new_state.apps.get_model("core", "TrashEntry")

    assert TrashEntry.objects.filter(trash_item_type="group").count() == 0
    assert TrashEntry.objects.filter(trash_item_type="workspace").count() == 1


@pytest.mark.django_db
def test_0053_migrate_group_trash_item_type_backwards():
    # Migrate `TrashEntry.trash_item_type` backwards from "group" to "workspace".
    migrate_from = [
        ("core", "0053_migrate_group_trash_item_type"),
    ]
    migrate_to = [
        ("core", "0052_auto_20230130_1118"),
    ]

    old_state = migrate(migrate_from)

    Workspace = old_state.apps.get_model("core", "Workspace")
    workspace = Workspace.objects.create(name="My workspace")
    TrashEntry = old_state.apps.get_model("core", "TrashEntry")

    TrashEntry.objects.create(
        workspace=workspace, trash_item_id=workspace.id, trash_item_type="workspace"
    )

    assert TrashEntry.objects.filter(trash_item_type="group").count() == 0
    assert TrashEntry.objects.filter(trash_item_type="workspace").count() == 1

    new_state = migrate(migrate_to)

    TrashEntry = new_state.apps.get_model("core", "TrashEntry")

    assert TrashEntry.objects.filter(trash_item_type="group").count() == 1
    assert TrashEntry.objects.filter(trash_item_type="workspace").count() == 0
