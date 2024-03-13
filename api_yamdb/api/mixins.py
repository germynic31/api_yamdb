from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from reviews.validators import validate_username
from .permissions import IsAdminOrReadOnly


class ListDestroyCreateMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class ValidateUsernameMixin:

    @staticmethod
    def validate_username(username):
        return validate_username(username)
