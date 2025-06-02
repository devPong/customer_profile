
from django.urls import path, include

urlpatterns = [
    path('core', include('sys_core.urls',namespace="core")),
    path('api', include('sys_api.urls',namespace="api")),
    path('app', include('web_app.urls',namespace="app")),
    
]
