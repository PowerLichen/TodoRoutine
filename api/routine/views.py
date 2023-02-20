from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.routine import schemas
from api.routine.serializers import RoutineSerializer
from api.routine.serializers import RoutineCreateSerializer
from api.routine.serializers import RoutineUpdateSerializer
from model.routine.models import Routine

@extend_schema_view(
    create=schemas.SCHEMA_ROUTINE_CREATE,
)
@extend_schema(tags=['routine'])
class RoutineViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Routine.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RoutineCreateSerializer
        if self.action == 'partial_update':
            return RoutineUpdateSerializer
        
        return RoutineSerializer
