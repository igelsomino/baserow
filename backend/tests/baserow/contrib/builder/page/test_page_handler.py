from django.db import IntegrityError

import pytest

from baserow.contrib.builder.page.handler import PageHandler
from baserow.contrib.builder.page.model import Page
from baserow.core.exceptions import UserNotInGroup


@pytest.mark.django_db
def test_create_page(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)

    page = PageHandler().create_page(user, builder, "test")

    assert page.builder is builder
    assert page.name == "test"
    assert page.order == 1
    assert Page.objects.count() == 1


@pytest.mark.django_db(transaction=True)
def test_create_page_same_page_name(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)

    name = "test"

    PageHandler().create_page(user, builder, name)

    with pytest.raises(IntegrityError):
        PageHandler().create_page(user, builder, name)

    assert Page.objects.count() == 1


@pytest.mark.django_db
def test_create_page_user_not_in_group(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application()

    with pytest.raises(UserNotInGroup):
        PageHandler().create_page(user, builder, "test")


@pytest.mark.django_db
def test_delete_page(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)

    page = PageHandler().create_page(user, builder, "test")

    PageHandler().delete_page(user, page)

    assert Page.objects.count() == 0


@pytest.mark.django_db(transaction=True)
def test_delete_page(data_fixture):
    user = data_fixture.create_user()
    user_unrelated = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)

    page = PageHandler().create_page(user, builder, "test")

    with pytest.raises(UserNotInGroup):
        PageHandler().delete_page(user_unrelated, page)

    assert Page.objects.count() == 1
