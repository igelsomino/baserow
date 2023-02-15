import pytest

from baserow.contrib.builder.elements.exceptions import ElementDoesNotExist
from baserow.contrib.builder.elements.handler import ElementHandler
from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.elements.registries import element_type_registry


@pytest.mark.django_db
def test_create_element(data_fixture):
    page = data_fixture.create_builder_page()

    for index, element_type in enumerate(element_type_registry.get_all()):
        sample_params = element_type.get_sample_params()

        element = ElementHandler().create_element(
            element_type, page=page, **sample_params
        )

        assert element.page.id == page.id

        for key, value in sample_params.items():
            assert getattr(element, key) == value

        assert element.order == index + 1
        assert Element.objects.count() == index + 1


@pytest.mark.django_db
def test_get_element(data_fixture):
    element = data_fixture.create_builder_header_element()

    assert ElementHandler().get_element(element.id).id == element.id


@pytest.mark.django_db
def test_get_element_does_not_exist(data_fixture):
    with pytest.raises(ElementDoesNotExist):
        assert ElementHandler().get_element(0)


@pytest.mark.django_db
def test_get_elements(data_fixture):
    page = data_fixture.create_builder_page()
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(page=page)

    assert [p.id for p in ElementHandler().get_elements(page)] == [
        element1.id,
        element2.id,
        element3.id,
    ]


@pytest.mark.django_db
def test_delete_element(data_fixture):
    element = data_fixture.create_builder_header_element()

    ElementHandler().delete_element(element)

    assert Element.objects.count() == 0


@pytest.mark.django_db
def test_update_element(data_fixture):
    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    element_updated = ElementHandler().update_element(
        element, {"config": {"value": "newValue"}}
    )

    assert element_updated.config == {"value": "newValue"}


@pytest.mark.django_db
def test_update_element_invalid_values(data_fixture):
    element = data_fixture.create_builder_header_element()

    element_updated = ElementHandler().update_element(
        element, {"config": {"nonsense": "hello"}}
    )

    assert not hasattr(element_updated, "nonsense")


@pytest.mark.django_db
def test_order_elements(data_fixture):
    page = data_fixture.create_builder_page()
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(page=page)

    ElementHandler().order_elements(page, [element3.id, element1.id])

    first, second, third = Element.objects.all()

    assert first.id == element2.id
    assert second.id == element3.id
    assert third.id == element1.id
