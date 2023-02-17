from django.urls import path
from django.urls import include

urlpatterns = [
    path("auth/", include("api.auth.urls")),
    path('routine/', include('api.routine.urls')),
]
