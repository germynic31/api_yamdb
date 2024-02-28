from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title, Category, Genre
from .mixins import ListDestroyCreateMixin
from .serializers import (
    CategorySerializer,
    GenreSerializer, CreateUpdateDestroyTitleSerializer,
    ListRetrieveTitleSerializer,
)


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
