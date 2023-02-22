import datetime

from django.db.models import F
from django.db.models import Q
from django.db.models import FilteredRelation
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import ParseError
from rest_framework.viewsets import GenericViewSet

from api.routine import schemas
from api.routine.renderers import RoutineJSONRenderer
from api.routine.serializers import RoutineSerializer
from api.routine.serializers import RoutineCreateSerializer
from api.routine.serializers import RoutineUpdateSerializer
from api.routine.serializers import RoutineRetrieveSerializer
from api.routine.serializers import RoutineListSerializer
from api.routine.serializers import RoutineDestroySerializer
from model.routine.models import Routine
from model.routine.models import RoutineDay


@extend_schema_view(
    create=schemas.SCHEMA_ROUTINE_CREATE,
    partial_update=schemas.SCHEMA_ROUTINE_UPDATE,
    retrieve=schemas.SCHEMA_ROUTINE_RETRIEVE,
    list=schemas.SCHEMA_ROUTINE_LIST,
)
@extend_schema(tags=["routine"])
class RoutineViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Routine.objects.all()
    renderer_classes = [RoutineJSONRenderer]
    
    def _queryset_filter_by_date(self, date):
        today = datetime.date.fromisoformat(date)
        cur_weekday = RoutineDay.WEEKDAY_CHOICES[today.weekday()][0]
        
        queryset = (
            super()
            .get_queryset()
            .annotate(
                today_routine_result=FilteredRelation(
                    "routine_result_set",
                    condition=Q(routine_result_set__created_at__date=today)
                )
            )
            .filter(routine_day_set__day=cur_weekday)
            .values(
                "routine_id","goal", "account_id", "title",
                result=F("today_routine_result__result")
            )
        )
            
        return queryset
    
    def get_queryset(self):
        if self.action == "list":
            date = self.request.data.get("today", None)
            if date is None:
                raise ParseError
            
            return self._queryset_filter_by_date(date)
            
        return super().get_queryset()
    
    def get_serializer_class(self):
        if self.action == "create":
            return RoutineCreateSerializer
        if self.action == "partial_update":
            return RoutineUpdateSerializer
        if self.action == "retrieve":
            return RoutineRetrieveSerializer
        if self.action == "list":
            return RoutineListSerializer
        if self.action == "destroy":
            return RoutineDestroySerializer
        
        return RoutineSerializer

    def destroy(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
