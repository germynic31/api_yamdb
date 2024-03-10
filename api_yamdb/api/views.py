from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from user.permissions import IsAdminOrReadOnly, IsModerOrReadOnly
from reviews.models import Title, Category, Genre, Review
from .filter_sets import TitleFilter
from .mixins import ListDestroyCreateMixin
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateUpdateDestroyTitleSerializer, GenreSerializer,
                          ListRetrieveTitleSerializer, ReviewSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        return get_object_or_404(
            Title, id=self.kwargs.get('title_id')).reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(title=title, author=self.request.user)

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PATCH']:
            return (IsModerOrReadOnly(),)
        return (IsAuthenticatedOrReadOnly(),)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id')).comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review=review, author=self.request.user)

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PATCH']:
            return (IsModerOrReadOnly(),)
        return (IsAuthenticatedOrReadOnly(),)
