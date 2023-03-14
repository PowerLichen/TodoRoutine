from django.db import models

from model.core.managers import ActiveManager


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("created", auto_now_add=True, editable=False)
    modified_at = models.DateTimeField("modified", auto_now=True, editable=False)
    
    class Meta:
        abstract = True


class DeletedAndTimeStampedModel(TimeStampedModel):
    is_deleted = models.BooleanField("deleted", default=False)
    
    objects = models.Manager()
    active_objects = ActiveManager()
    
    class Meta:
        abstract = True
