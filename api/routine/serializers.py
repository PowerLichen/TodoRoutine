from rest_framework import serializers

from model.routine.models import Routine
from model.routine.models import RoutineDay
from model.routine.models import RoutineResult


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ["routine_id", "account_id", "title", "category", "goal", "is_alarm"]
        