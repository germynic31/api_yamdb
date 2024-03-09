from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from user.validators import validate_username
from user.permissions import IsAdminOrReadOnly


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


class ValidateUsernameMixin:

    def validate_username(self, username):
        return validate_username(username)
