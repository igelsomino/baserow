from baserow_premium.views.models import CalendarViewFieldOptions
from rest_framework import serializers


class CalendarViewFieldOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarViewFieldOptions
        fields = ("hidden", "order")


class ListCalendarRowsQueryParamsSerializer(serializers.Serializer):
    # TODO: validations
    from_timestamp = serializers.DateTimeField(required=True)
    to_timestamp = serializers.DateTimeField(required=True)
    offset = serializers.IntegerField(default=0)
    limit = serializers.IntegerField(default=40)
