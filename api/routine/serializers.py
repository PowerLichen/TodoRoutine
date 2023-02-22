from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotFound

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
        
    def _get_lastest_result_date(self, obj):
        result = None
        today = timezone.localdate()
        today_weekday = today.weekday()
        target_weekday = [dayset.day for dayset in obj.routine_day_set.all()]
        for i in range(7):
            cur_weekday = (today_weekday - i) % 7
            if RoutineDay.WEEKDAY_CHOICES[cur_weekday][0] in target_weekday:
                result = i
                break
        
        return result

    def get_result(self, obj):
        target_daydiff = self._get_lastest_result_date(obj)
        if target_daydiff is None:
            raise NotFound()
        
        target_date = timezone.localdate() - timedelta(days=target_daydiff)
        status = obj.routine_result_set \
            .filter(created_at__date=target_date) \
            .order_by("-created_at") \
            .first()
        if status is not None:
            return status.result
        return "NOT"


class RoutineListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='account_id', read_only=True)
    result = serializers.SerializerMethodField()

    class Meta:
        model = Routine
        fields = ["goal", "id", "result", "title"]

    def get_result(self, obj):
        if obj["result"] is None:
            return "NOT"        
        return obj["result"]


class RoutineDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ["routine_id"]
    
    def update(self, instance, validated_data):
        for item in instance.routine_result_set.all():
            setattr(item, "is_deleted", True)
            item.save()
            
        setattr(instance, "is_deleted", True)
        instance.save()  
        return instance


class RoutineResultUpdateSerializer(serializers.Serializer):
    today = serializers.DateField()
    result = serializers.ChoiceField(choices=RoutineResult.RESULT_CHOICES)
        
    def update(self, instance, validated_data):
        weekday_num = validated_data["today"].weekday()
        weekday_str = RoutineDay.WEEKDAY_CHOICES[weekday_num][0]
        
        valid_routine_day = instance.routine_day_set.all().filter(day=weekday_str)
        if len(valid_routine_day) == 0:
            raise NotFound
        
        obj, created = instance.routine_result_set.update_or_create(
            created_at__date=validated_data["today"],
            defaults={
                "result": validated_data["result"]
            }
        )
        
        if created == True:
            obj.created_at = validated_data["today"]
            
        obj.save()
        return obj
    
    def to_representation(self, instance):
        return {"routine_result_id": instance.routine_result_id}
