from django.urls import path, include
from rest_framework import routers

from .views import TitleViewSet, GenreViewSet, CategoryViewSet
from user.views import EmailViewSet, UserViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('auth/signup', EmailViewSet, basename='singup')


urlpatterns = [
    path('v1/', include(router_v1.urls))
]
