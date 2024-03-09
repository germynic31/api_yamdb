from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from user.validators import validate_username


class ListDestroyCreateMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (SearchFilter,)
    pagination_class = LimitOffsetPagination


class ValidateUsernameMixin:
    def validate_username(self, username):
        return validate_username(username)
