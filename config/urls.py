from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularJSONAPIView
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema"),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include('api.urls')),
]
