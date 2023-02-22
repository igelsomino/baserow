from pytz import all_timezones
from pytz import timezone as pytz_timezone
from requests.exceptions import RequestException
from rest_framework import serializers

from baserow.api.applications.serializers import ApplicationSerializer
from baserow.api.errors import ERROR_GROUP_DOES_NOT_EXIST, ERROR_USER_NOT_IN_GROUP
from baserow.contrib.database.airtable.exceptions import (
    AirtableBaseNotPublic,
    AirtableShareIsNotABase,
)
from baserow.contrib.database.airtable.models import AirtableImportJob
from baserow.contrib.database.airtable.operations import (
    RunAirtableImportJobOperationType,
)
from baserow.contrib.database.airtable.utils import extract_share_id_from_url
from baserow.contrib.database.airtable.validators import is_publicly_shared_airtable_url
from baserow.core.action.registries import action_type_registry
from baserow.core.exceptions import UserNotInWorkspace, WorkspaceDoesNotExist
from baserow.core.handler import CoreHandler
from baserow.core.jobs.registries import JobType
from baserow.core.signals import application_created

from .actions import ImportDatabaseFromAirtableActionType


class AirtableImportJobType(JobType):
    type = "airtable"

    model_class = AirtableImportJob

    max_count = 1

    api_exceptions_map = {
        UserNotInWorkspace: ERROR_USER_NOT_IN_GROUP,
        WorkspaceDoesNotExist: ERROR_GROUP_DOES_NOT_EXIST,
    }

    job_exceptions_map = {
        RequestException: "The Airtable server could not be reached.",
        AirtableBaseNotPublic: "The Airtable base is not publicly shared.",
        AirtableShareIsNotABase: "The shared link is not a base. It's probably a "
        "view and the Airtable import tool only supports shared bases.",
    }

    request_serializer_field_names = [
        "group_id",  # GroupDeprecation
        "workspace_id",
        "database_id",
        "timezone",
        "airtable_share_url",
    ]

    request_serializer_field_overrides = {
        # GroupDeprecation
        "group_id": serializers.IntegerField(
            help_text="The workspace ID where the Airtable base must be imported into.",
        ),
        "workspace_id": serializers.IntegerField(
            help_text="The workspace ID where the Airtable base must be imported into.",
        ),
        "airtable_share_url": serializers.URLField(
            validators=[is_publicly_shared_airtable_url],
            help_text="The publicly shared URL of the Airtable base (e.g. "
            "https://airtable.com/shrxxxxxxxxxxxxxx)",
        ),
        "timezone": serializers.ChoiceField(
            required=False,
            choices=all_timezones,
            help_text="Optionally a timezone can be provided that must be respected "
            "during import. This is for example setting the correct value of the date "
            "fields.",
        ),
    }

    serializer_field_names = [
        "group_id",  # GroupDeprecation
        "workspace_id",
        "database",
        "airtable_share_id",
        "timezone",
    ]

    serializer_field_overrides = {
        # GroupDeprecation
        "group_id": serializers.IntegerField(
            help_text="The workspace ID where the Airtable base must be imported into.",
        ),
        "workspace_id": serializers.IntegerField(
            help_text="The workspace ID where the Airtable base must be imported into.",
        ),
        "airtable_share_id": serializers.URLField(
            max_length=18,
            help_text="Public ID of the shared Airtable base that must be imported.",
        ),
        "timezone": serializers.CharField(
            help_text="Optionally a timezone can be provided that must be respected "
            "during import. This is for example setting the correct value of the date "
            "fields.",
        ),
        "database": ApplicationSerializer(),
    }

    def prepare_values(self, values, user):

        workspace = CoreHandler().get_workspace(values.pop("workspace_id"))
        CoreHandler().check_permissions(
            user,
            RunAirtableImportJobOperationType.type,
            workspace=workspace,
            context=workspace,
        )

        airtable_share_id = extract_share_id_from_url(values["airtable_share_url"])
        timezone = values.get("timezone")

        if timezone is not None:
            timezone = pytz_timezone(timezone)

        return {
            "airtable_share_id": airtable_share_id,
            "timezone": timezone,
            "workspace": workspace,
        }

    def run(self, job, progress):

        kwargs = {}

        if job.timezone is not None:
            kwargs["timezone"] = pytz_timezone(job.timezone)

        database = action_type_registry.get(
            ImportDatabaseFromAirtableActionType.type
        ).do(
            job.user,
            job.group,
            job.airtable_share_id,
            progress_builder=progress.create_child_builder(
                represents_progress=progress.total
            ),
            **kwargs,
        )

        application_created.send(self, application=database, user=None)

        job.database = database
        job.save(update_fields=("database",))
