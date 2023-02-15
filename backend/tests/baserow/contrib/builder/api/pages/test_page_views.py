from django.urls import reverse

import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_page(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application(user=user)

    name = "test"

    url = reverse("api:builder:pages:list", kwargs={"builder_id": builder.id})
    response = api_client.post(
        url, {"name": name}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == name


@pytest.mark.django_db
def test_create_page_user_not_in_group(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application()

    url = reverse("api:builder:pages:list", kwargs={"builder_id": builder.id})
    response = api_client.post(
        url, {"name": "test"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_USER_NOT_IN_GROUP"


@pytest.mark.django_db
def test_create_page_application_does_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    url = reverse("api:builder:pages:list", kwargs={"builder_id": 9999})
    response = api_client.post(
        url, {"name": "test"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_APPLICATION_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_update_page(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(builder=builder, name="something")

    url = reverse(
        "api:builder:pages:item", kwargs={"builder_id": builder.id, "page_id": page.id}
    )
    response = api_client.patch(
        url, {"name": "test"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["name"] == "test"


@pytest.mark.django_db
def test_update_page_application_does_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(builder=builder, name="something")

    url = reverse(
        "api:builder:pages:item", kwargs={"builder_id": 9999, "page_id": page.id}
    )
    response = api_client.patch(
        url, {"name": "test"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_APPLICATION_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_update_page_page_does_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application(user=user)

    url = reverse(
        "api:builder:pages:item", kwargs={"builder_id": builder.id, "page_id": 9999}
    )
    response = api_client.patch(
        url, {"name": "test"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_PAGE_DOES_NOT_EXIST"
