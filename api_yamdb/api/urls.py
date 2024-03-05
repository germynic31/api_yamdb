from django.urls import path, include
from rest_framework import routers


from .views import ReviewViewSet, CommentViewSet, TitleViewSet, GenreViewSet, CategoryViewSet
from user.views import UserViewSet, SignupView, TokenView


router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews'
                   r'/(?P<review_id>\d+)/comments',
                   CommentViewSet, basename='comments')
router_v1.register('users/', UserViewSet, basename='users')
router_v1.register('users/me', UserViewSet, basename='me')
router_v1.register(r'/(users/?P<user_username>\d+)', UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/signup/', SignupView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
    path('v1/', include(router_v1.urls)),
]
