from django.conf import settings
from django.db import models

from model.core.models import DeletedAndTimeStampedModel
from model.core.models import TimeStampedModel


class Routine(DeletedAndTimeStampedModel):
    CATEGORY_CHOICES = (
        ('MIRACLE', 'MIRACLE'),
        ('HOMEWORK', 'HOMEWORK'),
    )
    
    routine_id = models.BigAutoField(primary_key=True)
    account_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=8, choices=CATEGORY_CHOICES)
    goal = models.TextField()
    is_alarm = models.BooleanField('alarm', default=False)
    
    class Meta:
        db_table = 'routine'


class RoutineResult(DeletedAndTimeStampedModel): 
    RESULT_CHOICES = (
        ('NOT', 'NOT'),
        ('TRY', 'TRY'),
        ('DONE', 'DONE'),
    )
       
    routine_result_id = models.BigAutoField(primary_key=True)
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE)
    result = models.CharField(max_length=4, choices=RESULT_CHOICES)
    
    class Meta:
        db_table = 'routine_result'
        
        
class RoutineDay(TimeStampedModel):
    WEEKDAY_CHOICES = (
        ("SUN", "SUN"),
        ("MON", "MON"),
        ("TUE", "TUE"),
        ("WED", "WED"),
        ("THU", "THU"),
        ("FRI", "FRI"),
        ("SAT", "SAT")
    )
    day = models.CharField(max_length=3, choices=WEEKDAY_CHOICES)
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "routine_day"
