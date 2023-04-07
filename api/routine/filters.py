from django_filters import rest_framework as filters
from django.db.models import F
from django.db.models import FilteredRelation
from django.db.models import Q

from model.routine.choices import WEEKDAY_CHOICES
from model.routine.models import Routine


class RoutineFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_class(self, view, queryset=None):
        if view.action == "list":
            return RoutineListFilter
        return super().get_filterset_class(view, queryset)


class RoutineListFilter(filters.FilterSet):
    today = filters.DateFilter(
        field_name="created_at",
        method="get_filter_by_date",
        required=True
    )
    
    def get_filter_by_date(self, queryset, field_name, value):
        today = value
        cur_weekday = WEEKDAY_CHOICES[today.weekday()][0]
        
        queryset = (
            queryset
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
    
    class Meta:
        model = Routine
        fields = ["today"]