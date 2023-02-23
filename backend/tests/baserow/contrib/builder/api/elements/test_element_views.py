from django.urls import reverse

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


@pytest.mark.django_db
def test_create_element(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)

    url = reverse("api:builder:element:list", kwargs={"page_id": page.id})
    response = api_client.post(
        url,
        {"type": "header"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["type"] == "header"


# @TODO finish tests

@pytest.mark.django_db
def test_create_element_user_not_in_group(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application()

    url = reverse(
        "api:builder:builder_id:pages:list", kwargs={"builder_id": builder.id}
    )
    response = api_client.post(
        url, {"name": "test"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_USER_NOT_IN_GROUP"


@pytest.mark.django_db
def test_create_element_application_does_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    url = reverse("api:builder:builder_id:pages:list", kwargs={"builder_id": 9999})
    response = api_client.post(
        url, {"name": "test"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_APPLICATION_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_update_element(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_element(builder=builder, name="something")

    url = reverse("api:builder:pages:item", kwargs={"page_id": page.id})
    response = api_client.patch(
        url, {"name": "test"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["name"] == "test"


@pytest.mark.django_db
def test_update_element_element_does_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    url = reverse("api:builder:pages:item", kwargs={"page_id": 9999})
    response = api_client.patch(
        url, {"name": "test"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_PAGE_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_order_elements(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application(user=user)
    page_one = data_fixture.create_builder_element(builder=builder, order=1)
    page_two = data_fixture.create_builder_element(builder=builder, order=2)

    url = reverse(
        "api:builder:builder_id:pages:order", kwargs={"builder_id": builder.id}
    )
    response = api_client.post(
        url,
        {"page_ids": [page_two.id, page_one.id]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_order_elements_user_not_in_group(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application()
    page_one = data_fixture.create_builder_element(builder=builder, order=1)
    page_two = data_fixture.create_builder_element(builder=builder, order=2)

    url = reverse(
        "api:builder:builder_id:pages:order", kwargs={"builder_id": builder.id}
    )
    response = api_client.post(
        url,
        {"page_ids": [page_two.id, page_one.id]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_USER_NOT_IN_GROUP"


@pytest.mark.django_db
def test_order_elements_element_not_in_builder(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application(user=user)
    page_one = data_fixture.create_builder_element(builder=builder, order=1)
    page_two = data_fixture.create_builder_element(order=2)

    url = reverse(
        "api:builder:builder_id:pages:order", kwargs={"builder_id": builder.id}
    )
    response = api_client.post(
        url,
        {"page_ids": [page_two.id, page_one.id]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_PAGE_NOT_IN_BUILDER"


@pytest.mark.django_db
def test_order_elements_application_does_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application(user=user)
    page_one = data_fixture.create_builder_element(builder=builder, order=1)
    page_two = data_fixture.create_builder_element(builder=builder, order=2)

    url = reverse("api:builder:builder_id:pages:order", kwargs={"builder_id": 99999})
    response = api_client.post(
        url,
        {"page_ids": [page_two.id, page_one.id]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_APPLICATION_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_delete_element(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_element(builder=builder, order=1)

    url = reverse("api:builder:pages:item", kwargs={"page_id": page.id})
    response = api_client.delete(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_element_user_not_in_group(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application()
    page = data_fixture.create_builder_element(builder=builder, order=1)

    url = reverse("api:builder:pages:item", kwargs={"page_id": page.id})
    response = api_client.delete(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_USER_NOT_IN_GROUP"


@pytest.mark.django_db
def test_delete_element_element_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    url = reverse("api:builder:pages:item", kwargs={"page_id": 99999})
    response = api_client.delete(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_PAGE_DOES_NOT_EXIST"
