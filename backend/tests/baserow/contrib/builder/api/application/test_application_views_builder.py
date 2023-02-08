from django.urls import reverse

import pytest
from rest_framework.status import HTTP_200_OK

from baserow.contrib.builder.application_types import BuilderApplicationType
from baserow.contrib.builder.models import Builder


@pytest.mark.django_db
def test_can_create_a_builder_application(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    group = data_fixture.create_group(user=user)

    response = api_client.post(
        reverse("api:applications:list", kwargs={"group_id": group.id}),
        {"name": "Test 1", "type": BuilderApplicationType.type},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    builder = Builder.objects.all()[0]

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["type"] == BuilderApplicationType.type
    assert response_json["id"] == builder.id
    assert response_json["name"] == builder.name
    assert response_json["order"] == builder.order
