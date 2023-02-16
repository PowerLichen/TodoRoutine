from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("created", auto_now_add=True, editable=False)
    modified_at = models.DateTimeField("modified", auto_now=True, editable=False)
    
    class Meta:
        abstract = True
        
class DeletedAndTimeStampedModel(TimeStampedModel):
    is_deleted = models.BooleanField("deleted", default=False)
    
    class Meta:
        abstract = True
