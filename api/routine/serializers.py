from django.contrib.auth import get_user_model
from rest_framework import serializers

from model.routine.models import Routine
from model.routine.models import RoutineDay
from model.routine.models import RoutineResult


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ["routine_id", "account_id", "title", "category", "goal", "is_alarm"]


class RoutineCreateSerializer(serializers.ModelSerializer):
    account = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    days = serializers.MultipleChoiceField(choices=RoutineDay.WEEKDAY_CHOICES)
    
    class Meta:
        model = Routine
        fields = ["account", "title", "category", "goal", "is_alarm", "days"]
        
    
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
            "routine_id": instance.routine_id
        }


class RoutineUpdateSerializer(serializers.ModelSerializer):
    days = serializers.MultipleChoiceField(choices=RoutineDay.WEEKDAY_CHOICES)
    
    class Meta:
        model = Routine
        fields = ["routine_id", "title", "category", "goal", "is_alarm", "days"]
    
    def _update_day_routine(self, instance, weekday_lst):
        instance.routine_day_set.exclude(day__in=weekday_lst).delete()
        
        for weekday in weekday_lst:
            instance.routine_day_set.get_or_create(day=weekday)
        
        instance.save()
        
    def update(self, instance, validated_data):
        custom_data = validated_data
        weekday_lst = custom_data.pop("days", None)
        
        if weekday_lst is not None:
            self._update_day_routine(instance, weekday_lst)
        
        return super().update(instance, custom_data)
    
    def to_representation(self, instance):
        return {
            "routine_id": instance.routine_id
        }


class RoutineRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='account_id', read_only=True)
    days = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        source="routine_day_set",
        slug_field="day"
    )
    result = serializers.SerializerMethodField()
    
    class Meta:
        model = Routine
        fields = ["goal", "id", "result", "title", "days"]

    def get_result(self, obj):
        status = obj.routine_result_set \
            .order_by("-created_at") \
            .first()
        if status is not None:
            return status.result
        return "NOT"
