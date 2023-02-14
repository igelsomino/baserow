from django.db import transaction

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from baserow.api.applications.errors import ERROR_APPLICATION_DOES_NOT_EXIST
from baserow.api.decorators import map_exceptions, validate_body
from baserow.api.errors import ERROR_USER_NOT_IN_GROUP
from baserow.api.schemas import CLIENT_SESSION_ID_SCHEMA_PARAMETER, get_error_schema
from baserow.contrib.builder.api.pages.serializers import (
    CreatePageSerializer,
    PageSerializer,
)
from baserow.contrib.builder.handler import BuilderHandler
from baserow.contrib.builder.page.handler import PageHandler
from baserow.contrib.builder.page.operations import CreatePageOperationType
from baserow.core.exceptions import ApplicationDoesNotExist, UserNotInGroup
from baserow.core.handler import CoreHandler


class PageView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="builder_id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
                description="Creates a page for the application builder related to the "
                "provided value.",
            ),
            CLIENT_SESSION_ID_SCHEMA_PARAMETER,
        ],
        tags=["Builder pages"],
        operation_id="create_builder_page",
        description="Creates a new page for an application builder",
        request=CreatePageSerializer,
        responses={
            200: PageSerializer,
            400: get_error_schema(
                [
                    "ERROR_USER_NOT_IN_GROUP",
                    "ERROR_REQUEST_BODY_VALIDATION",
                ]
            ),
            404: get_error_schema(["ERROR_APPLICATION_DOES_NOT_EXIST"]),
        },
    )
    @transaction.atomic
    @map_exceptions(
        {
            ApplicationDoesNotExist: ERROR_APPLICATION_DOES_NOT_EXIST,
            UserNotInGroup: ERROR_USER_NOT_IN_GROUP,
        }
    )
    @validate_body(CreatePageSerializer)
    def post(self, request, data, builder_id):
        builder = BuilderHandler().get_builder(builder_id).specific

        CoreHandler().check_permissions(
            request.user,
            CreatePageOperationType.type,
            group=builder.group,
            context=builder,
        )

        page = PageHandler().create_page(request.user, builder, data["name"])

        serializer = PageSerializer(page)
        return Response(serializer.data)
