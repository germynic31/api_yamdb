from django.urls import path, include
from rest_framework import routers


router_v1 = routers.DefaultRouter()


urlpatterns = [
    path('v1/', include(router_v1.urls))
]
