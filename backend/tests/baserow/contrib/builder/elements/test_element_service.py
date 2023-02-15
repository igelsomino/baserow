import pytest

from baserow.contrib.builder.elements.exceptions import (
    ElementDoesNotExist,
    ElementNotInPage,
)
from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.elements.registries import element_type_registry
from baserow.contrib.builder.elements.service import ElementService
from baserow.core.exceptions import UserNotInGroup


@pytest.mark.django_db
def test_create_element(data_fixture):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)

    for index, element_type in enumerate(element_type_registry.get_all()):
        sample_params = element_type.get_sample_params()

        element = ElementService().create_element(
            user, element_type, page=page, **sample_params
        )

        assert element.page.id == page.id

        for key, value in sample_params.items():
            assert getattr(element, key) == value

        assert element.order == index + 1
        assert Element.objects.count() == index + 1


@pytest.mark.django_db
def test_create_element_user_not_in_group(data_fixture):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page()

    element_type = element_type_registry.get("header")

    with pytest.raises(UserNotInGroup):
        ElementService().create_element(
            user, element_type, page=page, **element_type.get_sample_params()
        )


@pytest.mark.django_db
def test_get_element(data_fixture):
    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    assert ElementService().get_element(user, element.id).id == element.id


@pytest.mark.django_db
def test_get_element_does_not_exist(data_fixture):
    user = data_fixture.create_user()

    with pytest.raises(ElementDoesNotExist):
        assert ElementService().get_element(user, 0)


@pytest.mark.django_db
def test_get_element_user_not_in_group(data_fixture):
    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element()

    with pytest.raises(UserNotInGroup):
        ElementService().get_element(user, element.id)


@pytest.mark.django_db
def test_get_elements(data_fixture):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(page=page)

    assert [p.id for p in ElementService().get_elements(user, page)] == [
        element1.id,
        element2.id,
        element3.id,
    ]


@pytest.mark.django_db
def test_delete_element(data_fixture):
    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    ElementService().delete_element(user, element)

    assert Element.objects.count() == 0


@pytest.mark.django_db(transaction=True)
def test_delete_element_user_not_in_group(data_fixture):
    user = data_fixture.create_user()
    user_unrelated = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    with pytest.raises(UserNotInGroup):
        ElementService().delete_element(user_unrelated, element)

    assert Element.objects.count() == 1


@pytest.mark.django_db
def test_update_element(data_fixture):
    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    element_updated = ElementService().update_element(
        user, element, {"config": {"value": "newValue"}}
    )

    assert element_updated.config == {"value": "newValue"}


@pytest.mark.django_db
def test_update_element_user_not_in_group(data_fixture):
    user = data_fixture.create_user()
    user_unrelated = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    with pytest.raises(UserNotInGroup):
        ElementService().update_element(
            user_unrelated, element, {"config": {"value": "newValue"}}
        )


@pytest.mark.django_db
def test_update_element_invalid_values(data_fixture):

    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    element_updated = ElementService().update_element(
        user, element, {"config": {"nonsense": "hello"}}
    )

    assert not hasattr(element_updated, "nonsense")


@pytest.mark.django_db
def test_order_elements(data_fixture):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(page=page)

    ElementService().order_elements(user, page, [element3.id, element1.id])

    first, second, third = Element.objects.all()

    assert first.id == element2.id
    assert second.id == element3.id
    assert third.id == element1.id


@pytest.mark.django_db
def test_order_elements_user_not_in_group(data_fixture):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page()
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(page=page)

    with pytest.raises(UserNotInGroup):
        ElementService().order_elements(user, page, [element3.id, element1.id])


@pytest.mark.django_db
def test_order_elements_not_in_page(data_fixture):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(user=user)

    with pytest.raises(ElementNotInPage):
        ElementService().order_elements(user, page, [element3.id, element1.id])
