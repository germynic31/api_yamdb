from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser

from user.models import MyUser
from reviews.models import Title, Category, Genre
from .mixins import ListDestroyCreateMixin
from .serializers import (
    UserSerializer, CategorySerializer,
    GenreSerializer, CreateUpdateDestroyTitleSerializer,
    ListRetrieveTitleSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),) #TODO сделаю в другой ветке
        return super().get_permissions()


