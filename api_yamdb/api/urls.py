from django.urls import path, include
from rest_framework import routers

from .views import TitleViewSet, GenreViewSet, CategoryViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router_v1.urls))
]
