from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from user.models import MyUser
from reviews.models import Title, Category, Genre
from .mixins import ListDestroyCreateMixin
from .serializers import (
    UserSerializer, CategorySerializer,
    GenreSerializer, CreateUpdateDestroyTitleSerializer,
    ListRetrieveTitleSerializer, EmailConfirmSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

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


class EmailViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = EmailConfirmSerializer
    permission_classes = (IsAuthenticated, )

    def mail(self):
        token = default_token_generator.make_token(self.request.user)

        send_mail(
            subject='Код подтверждения',
            message=f'Токен для подтверждения: {token}',
            from_email='from@example.com',
            recipient_list=[self.request.user.email],
            fail_silently=True,
        )
