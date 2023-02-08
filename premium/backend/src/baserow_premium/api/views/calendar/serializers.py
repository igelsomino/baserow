from baserow_premium.views.models import CalendarViewFieldOptions
from rest_framework import serializers


class CalendarViewFieldOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarViewFieldOptions
        fields = ("hidden", "order")