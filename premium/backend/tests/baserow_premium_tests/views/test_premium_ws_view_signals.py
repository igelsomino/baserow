from unittest.mock import patch

import pytest

from baserow.contrib.database.views.handler import ViewHandler


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.registries.broadcast_to_channel_group")
def test_view_created_not_collaborative(mock_broadcast_to_channel_group, data_fixture, alternative_per_group_license_service):
    group = data_fixture.create_group(name="Group 1")
    user = data_fixture.create_user(group=group)
    database = data_fixture.create_database_application(group=group)
    table = data_fixture.create_database_table(user=user, database=database)
    alternative_per_group_license_service.restrict_user_premium_to(
        user, group.id
    )

    ViewHandler().create_view(
        user=user, table=table, type_name="grid", name="Grid", ownership_type="personal"
    )

    mock_broadcast_to_channel_group.delay.assert_not_called()


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.registries.broadcast_to_channel_group")
def test_view_updated_not_collaborative(mock_broadcast_to_channel_group, data_fixture, alternative_per_group_license_service):
    group = data_fixture.create_group(name="Group 1")
    user = data_fixture.create_user(group=group)
    database = data_fixture.create_database_application(group=group)
    table = data_fixture.create_database_table(user=user, database=database)
    alternative_per_group_license_service.restrict_user_premium_to(
        user, group.id
    )
    view = data_fixture.create_grid_view(user=user, table=table)
    view.ownership_type = "personal"
    view.created_by = user
    view.save()

    ViewHandler().update_view(user=user, view=view, name="View")

    mock_broadcast_to_channel_group.delay.assert_not_called()


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.registries.broadcast_to_channel_group")
def test_view_deleted_not_collaborative(mock_broadcast_to_channel_group, data_fixture, alternative_per_group_license_service):
    group = data_fixture.create_group(name="Group 1")
    user = data_fixture.create_user(group=group)
    database = data_fixture.create_database_application(group=group)
    table = data_fixture.create_database_table(user=user, database=database)
    alternative_per_group_license_service.restrict_user_premium_to(
        user, group.id
    )
    view = data_fixture.create_grid_view(user=user, table=table)
    view.ownership_type = "personal"
    view.created_by = user
    view.save()

    ViewHandler().delete_view(user=user, view=view)

    mock_broadcast_to_channel_group.delay.assert_not_called()