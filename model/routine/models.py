from django.conf import settings
from django.db import models

from model.core.models import DeletedAndTimeStampedModel


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
