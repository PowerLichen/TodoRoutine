from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.routine import schemas
from api.routine.renderers import RoutineJSONRenderer
from api.routine.serializers import RoutineSerializer
from api.routine.serializers import RoutineCreateSerializer
from api.routine.serializers import RoutineUpdateSerializer
from api.routine.serializers import RoutineRetrieveSerializer
from model.routine.models import Routine

@extend_schema_view(
    create=schemas.SCHEMA_ROUTINE_CREATE,
    partial_update=schemas.SCHEMA_ROUTINE_UPDATE,
    retrieve=schemas.SCHEMA_ROUTINE_RETRIEVE,
)
@extend_schema(tags=['routine'])
class RoutineViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Routine.objects.all()
    renderer_classes = [RoutineJSONRenderer]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RoutineCreateSerializer
        if self.action == 'partial_update':
            return RoutineUpdateSerializer
        if self.action == "retrieve":
            return RoutineRetrieveSerializer
        return RoutineSerializer
