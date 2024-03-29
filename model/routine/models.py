from django.conf import settings
from django.db import models

from model.core.models import DeletedAndTimeStampedModel
from model.core.models import TimeStampedModel
from model.routine.choices import CATEGORY_CHOICES
from model.routine.choices import RESULT_CHOICES
from model.routine.choices import WEEKDAY_CHOICES


class Routine(DeletedAndTimeStampedModel):    
    routine_id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="routine_set"
    )
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=8, choices=CATEGORY_CHOICES)
    goal = models.TextField()
    is_alarm = models.BooleanField("alarm", default=False)
    
    class Meta:
        db_table = "routine"


class RoutineResult(DeletedAndTimeStampedModel):       
    routine_result_id = models.BigAutoField(primary_key=True)
    routine = models.ForeignKey(
        Routine,
        on_delete=models.CASCADE,
        related_name="routine_result_set"
    )
    result = models.CharField(max_length=4, choices=RESULT_CHOICES)
    
    class Meta:
        db_table = "routine_result"
        
        
class RoutineDay(TimeStampedModel):    
    day = models.CharField(max_length=3, choices=WEEKDAY_CHOICES)
    routine = models.ForeignKey(
        Routine,
        on_delete=models.CASCADE,
        related_name="routine_day_set"
    )
    
    class Meta:
        db_table = "routine_day"
        constraints = [
            models.UniqueConstraint(
                fields=["day", "routine_id"],
                name="routine-day unique key"
            )            
        ]
