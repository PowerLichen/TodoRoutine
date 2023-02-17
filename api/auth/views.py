from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from api.auth.serializers import UserCreateSerializer


class UserCreateViewSet(mixins.CreateModelMixin,
                        GenericViewSet):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]