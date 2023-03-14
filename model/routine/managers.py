from django.db.models import F
from django.db.models import Q
from django.db.models import FilteredRelation
from django.db.models import Manager
from django.db.models import QuerySet

from model.routine.choices import WEEKDAY_CHOICES


class RoutineActiveQuerySet(QuerySet):
    def list_by_date(self, date):
        today = date
        cur_weekday = WEEKDAY_CHOICES[today.weekday()][0]
        queryset = (
            self
            .annotate(
                today_routine_result=FilteredRelation(
                    "routine_result_set",
                    condition=Q(routine_result_set__created_at__date=today)
                )
            )
            .filter(routine_day_set__day=cur_weekday)
            .filter(created_at__date__lte=today)
            .values(
                "routine_id",
                "goal",
                "account_id",
                "title",
                result=F("today_routine_result__result")
            )
        )
        
        return queryset


class RoutineActiveManager(Manager):
    def get_queryset(self):
        return RoutineActiveQuerySet(self.model, using=self._db).filter(is_deleted=False)
    
    def result_list(self, date):
        return self.get_queryset().list_by_date(date)
