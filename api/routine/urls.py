from django.urls import include
from django.urls import path
from rest_framework import routers

from api.routine import views

router = routers.DefaultRouter()
router.register(r'', views.RoutineViewSet, basename='notice')

urlpatterns = [
    path('', include(router.urls)),
]
