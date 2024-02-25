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
    permission_classes = IsAdminUser

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),) #TODO сделаю в другой ветке
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ListRetrieveTitleSerializer
        return CreateUpdateDestroyTitleSerializer


class GenreViewSet(ListDestroyCreateMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListDestroyCreateMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
