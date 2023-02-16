from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("created"), auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(_("modified"), auto_now=True, editable=False)
    
    class Meta:
        abstract = True
        
class DeletedAndTimeStampedModel(TimeStampedModel):
    is_deleted = models.BooleanField(_("deleted"), default=False)
