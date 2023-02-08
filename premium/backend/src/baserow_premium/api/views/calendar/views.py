from baserow_premium.license.features import PREMIUM
from baserow_premium.license.handler import LicenseHandler
from baserow_premium.views.handler import get_rows_grouped_by_single_select_field
from baserow_premium.views.models import CalendarView
from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from baserow.api.decorators import allowed_includes, map_exceptions
from baserow.api.errors import ERROR_USER_NOT_IN_GROUP
from baserow.api.schemas import get_error_schema
from baserow.contrib.database.api.rows.serializers import (
    RowSerializer,
    get_row_serializer_class,
)
from baserow.contrib.database.fields.field_filters import (
    FILTER_TYPE_AND,
    FILTER_TYPE_OR,
)
from baserow.contrib.database.table.operations import ListRowsDatabaseTableOperationType
from baserow.contrib.database.views.exceptions import (
    ViewDoesNotExist,
)
from baserow.contrib.database.views.handler import ViewHandler
from baserow.contrib.database.views.registries import view_type_registry
from baserow.core.exceptions import UserNotInGroup
from baserow.core.handler import CoreHandler
from baserow_premium.api.views.calendar.errors import ERROR_CALENDAR_VIEW_HAS_NO_DATE_FIELD
from baserow.contrib.database.api.views.errors import (
    ERROR_VIEW_DOES_NOT_EXIST,
    ERROR_VIEW_NOT_IN_TABLE,
)
from baserow_premium.views.exceptions import CalendarViewHasNoDateField
from baserow_premium.license.exceptions import FeaturesNotAvailableError


class CalendarViewView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="view_id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
                description="Returns only rows that belong to the related view's "
                "table.",
            ),
            OpenApiParameter(
                name="include",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                description="Accepts `field_options` as value if the field options "
                "must also be included in the response.",
            ),
            OpenApiParameter(
                name="limit",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
                description="Defines how many rows should be returned by default. "
                "This value can be overwritten per select option.",
            ),
            OpenApiParameter(
                name="offset",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
                description="Defines from which offset the rows should be returned."
                "This value can be overwritten per select option.",
            ),
        ],
        tags=["Database table calendar view"],
        operation_id="list_database_table_calendar_view_rows",
        # TODO:
        # description=(
        #     "Responds with serialized rows grouped by the view's single select field "
        #     "options if the user is authenticated and has access to the related "
        #     "group. Additional query parameters can be provided to control the "
        #     "`limit` and `offset` per select option."
        #     "\n\nThis is a **premium** feature."
        # ),
        responses={
            # TODO: docs
            # 200: KanbanViewExampleResponseSerializer,
            400: get_error_schema(
                [
                    "ERROR_USER_NOT_IN_GROUP",
                    "ERROR_CALENDAR_VIEW_HAS_NO_DATE_FIELD",
                    "ERROR_FEATURE_NOT_AVAILABLE",
                ]
            ),
            404: get_error_schema(["ERROR_VIEW_DOES_NOT_EXIST"]),
        },
    )
    @map_exceptions(
        {
            UserNotInGroup: ERROR_USER_NOT_IN_GROUP,
            ViewDoesNotExist: ERROR_VIEW_DOES_NOT_EXIST,
            CalendarViewHasNoDateField: (
                ERROR_CALENDAR_VIEW_HAS_NO_DATE_FIELD
            ),
        }
    )
    @allowed_includes("field_options")
    def get(self, request, view_id, field_options):
        # TODO: """Responds with the rows grouped by the view's select option field value."""

        view_handler = ViewHandler()
        view = view_handler.get_view_as_user(request.user, view_id, CalendarView)
        group = view.table.database.group

        # We don't want to check if there is an active premium license if the group
        # is a template because that feature must then be available for demo purposes.
        if not group.has_template():
            LicenseHandler.raise_if_user_doesnt_have_feature(
                PREMIUM, request.user, group
            )

        CoreHandler().check_permissions(
            request.user,
            ListRowsDatabaseTableOperationType.type,
            group=group,
            context=view.table,
            allow_if_template=True,
        )
        date_field = view.date_field

        if not date_field:
            raise CalendarViewHasNoDateField(
                "The requested calendar view does not have a required date field."
            )

        # (
        #     included_select_options,
        #     default_limit,
        #     default_offset,
        # ) = prepare_kanban_view_parameters(request)

        # model = view.table.get_model()
        # serializer_class = get_row_serializer_class(
        #     model, RowSerializer, is_response=True
        # )
        # rows = get_rows_grouped_by_single_select_field(
        #     view=view,
        #     single_select_field=single_select_option_field,
        #     option_settings=included_select_options,
        #     default_limit=default_limit,
        #     default_offset=default_offset,
        #     model=model,
        # )

        # for key, value in rows.items():
        #     rows[key]["results"] = serializer_class(value["results"], many=True).data

        # response = {"rows": rows}

        # if field_options:
        #     view_type = view_type_registry.get_by_model(view)
        #     context = {"fields": [o["field"] for o in model._field_objects.values()]}
        #     serializer_class = view_type.get_field_options_serializer_class(
        #         create_if_missing=True
        #     )
        #     response.update(**serializer_class(view, context=context).data)

        # return Response(response)
        return Response({})