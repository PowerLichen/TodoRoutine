from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from api.routine import schemas
from api.routine.filters import RoutineFilterBackend
from api.routine.renderers import RoutineJSONRenderer
from api.routine.serializers import RoutineSerializer
from api.routine.serializers import RoutineCreateSerializer
from api.routine.serializers import RoutineUpdateSerializer
from api.routine.serializers import RoutineRetrieveSerializer
from api.routine.serializers import RoutineListSerializer
from api.routine.serializers import RoutineDestroySerializer
from api.routine.serializers import RoutineResultUpdateSerializer
from model.routine.models import Routine


@extend_schema_view(
    create=schemas.SCHEMA_ROUTINE_CREATE,
    partial_update=schemas.SCHEMA_ROUTINE_UPDATE,
    retrieve=schemas.SCHEMA_ROUTINE_RETRIEVE,
    list=schemas.SCHEMA_ROUTINE_LIST,
    destroy=schemas.SCHEMA_ROUTINE_DESTROY,
    result=schemas.SCHEMA_ROUTINE_RESULT,
)
@extend_schema(tags=["routine"])
class RoutineViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Routine.active_objects.all()
    renderer_classes = [RoutineJSONRenderer]
    filter_backends = [RoutineFilterBackend, ]
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(account=self.request.user)
        return queryset
    
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
        if self.action == "result":
            return RoutineResultUpdateSerializer
        return RoutineSerializer

    def destroy(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], url_path='result')
    def result(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
