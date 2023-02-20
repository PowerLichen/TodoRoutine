from django.contrib.auth import get_user_model
from rest_framework import serializers

from model.routine.models import Routine
from model.routine.models import RoutineDay
from model.routine.models import RoutineResult


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ["routine_id", "account_id", "title", "category", "goal", "is_alarm"]


class RoutineCreateSerializer(serializers.Serializer):
    account_id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=get_user_model().objects.all(),
        default=serializers.CurrentUserDefault(),
        )
    title = serializers.CharField()
    category = serializers.ChoiceField(choices=Routine.CATEGORY_CHOICES)
    goal = serializers.CharField()
    is_alarm = serializers.BooleanField(default=False)
    days = serializers.MultipleChoiceField(choices=RoutineDay.WEEKDAY_CHOICES)
    
    def _create_day_routine(self, routine, weekday_lst):
        for weekday in weekday_lst:
            routine.routine_day_set.create(
                day=weekday
            )
    
    def create(self, validated_data):
        custom_data = validated_data
        weekday_lst = custom_data.pop("days")
        
        instance_routine = Routine.objects.create(**custom_data)
        self._create_day_routine(instance_routine, weekday_lst)
        
        instance_routine.save()
        return instance_routine
    
    def to_representation(self, instance):
        return {
            "data": {
                "routine_id": instance.routine_id
                },
            "message": {
                "msg": "You have successfully created the routine.",
                "status": "ROUTINE_CREATE_OK"
            }
        }
