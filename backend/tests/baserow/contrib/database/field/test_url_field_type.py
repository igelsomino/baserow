import pytest

from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.fields.field_types import URLFieldType


@pytest.mark.django_db
def test_airtable_import_url_field(data_fixture, api_client):
    airtable_field = {
        "id": "fldG9y88Zw7q7u4Z7i4",
        "name": "Name",
        "type": "text",
        "typeOptions": {"validatorName": "url"},
    }
    baserow_field, field_type = field_type_registry.from_airtable_field_to_serialized(
        airtable_field
    )
    assert baserow_field == {"type": URLFieldType.type}
    assert isinstance(field_type, URLFieldType)

    assert (
        field_type.from_airtable_column_value_to_serialized(
            {}, airtable_field, baserow_field, "NOT_URL", {}
        )
        == ""
    )
    assert (
        field_type.from_airtable_column_value_to_serialized(
            {}, airtable_field, baserow_field, "https://test.nl", {}
        )
        == "https://test.nl"
    )