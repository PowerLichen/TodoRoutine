from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.routine.serializers import RoutineSerializer
from model.routine.models import Routine


class RoutineViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Routine.objects.all()
    
    def get_serializer_class(self):
        return RoutineSerializer
