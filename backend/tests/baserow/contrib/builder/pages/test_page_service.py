from django.db import IntegrityError

import pytest

from baserow.contrib.builder.pages.exceptions import PageNotInBuilder
from baserow.contrib.builder.pages.models import Page
from baserow.contrib.builder.pages.service import PageService
from baserow.core.exceptions import UserNotInGroup


@pytest.mark.django_db
def test_create_page(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)

    page = PageService().create_page(user, builder, "test")

    assert page.builder is builder
    assert page.name == "test"
    assert page.order == 1
    assert Page.objects.count() == 1


@pytest.mark.django_db(transaction=True)
def test_create_page_same_page_name(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)

    name = "test"

    PageService().create_page(user, builder, name)

    with pytest.raises(IntegrityError):
        PageService().create_page(user, builder, name)

    assert Page.objects.count() == 1


@pytest.mark.django_db
def test_create_page_user_not_in_group(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application()

    with pytest.raises(UserNotInGroup):
        PageService().create_page(user, builder, "test")


@pytest.mark.django_db
def test_delete_page(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)

    page = PageService().create_page(user, builder, "test")

    PageService().delete_page(user, page)

    assert Page.objects.count() == 0


@pytest.mark.django_db(transaction=True)
def test_delete_page_user_not_in_group(data_fixture):
    user = data_fixture.create_user()
    user_unrelated = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)

    page = PageService().create_page(user, builder, "test")

    with pytest.raises(UserNotInGroup):
        PageService().delete_page(user_unrelated, page)

    assert Page.objects.count() == 1


@pytest.mark.django_db
def test_get_page(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(builder=builder)

    assert PageService().get_page(user, page.id).id == page.id


@pytest.mark.django_db
def test_get_page_user_not_in_group(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application()
    page = data_fixture.create_builder_page(builder=builder)

    with pytest.raises(UserNotInGroup):
        PageService().get_page(user, page.id)


@pytest.mark.django_db
def test_update_page(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(builder=builder)

    new_name = "test"

    page_updated = PageService().update_page(user, page, name=new_name)

    assert page_updated.name == new_name


@pytest.mark.django_db
def test_update_page_user_not_in_group(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application()
    page = data_fixture.create_builder_page(builder=builder)

    with pytest.raises(UserNotInGroup):
        PageService().update_page(user, page, name="test")


@pytest.mark.django_db
def test_update_page_invalid_values(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(builder=builder)

    page_updated = PageService().update_page(user, page, nonsense="hello")

    assert hasattr(page_updated, "nonsense") is False


@pytest.mark.django_db
def test_order_pages(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    page_one = data_fixture.create_builder_page(builder=builder, order=1)
    page_two = data_fixture.create_builder_page(builder=builder, order=2)

    PageService().order_pages(user, builder, [page_two.id, page_one.id])

    page_one.refresh_from_db()
    page_two.refresh_from_db()

    assert page_one.order > page_two.order


@pytest.mark.django_db
def test_order_pages_user_not_in_group(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application()
    page_one = data_fixture.create_builder_page(builder=builder, order=1)
    page_two = data_fixture.create_builder_page(builder=builder, order=2)

    with pytest.raises(UserNotInGroup):
        PageService().order_pages(user, builder, [page_two.id, page_one.id])


@pytest.mark.django_db
def test_order_pages_page_not_in_builder(data_fixture):
    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    page_one = data_fixture.create_builder_page(builder=builder, order=1)
    page_two = data_fixture.create_builder_page(order=2)

    with pytest.raises(PageNotInBuilder):
        PageService().order_pages(user, builder, [page_two.id, page_one.id])
