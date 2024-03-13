from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, SAFE_METHODS,
    AllowAny, IsAuthenticated
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Title, Category, Genre, Review
from reviews.models import User
from reviews.utils import generate_confirmation_code
from .permissions import IsAdminOrReadOnly, IsModerOrReadOnly, AdminOnly
from .filter_sets import TitleFilter
from .mixins import ListDestroyCreateMixin
from .serializers import (
    CategorySerializer, CommentSerializer, CreateUpdateDestroyTitleSerializer,
    GenreSerializer, ListRetrieveTitleSerializer, ReviewSerializer,
    MeSerializer, SignupSerializer, TokenSerializer, UserSerializer
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
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

    def get_title(self):
        if not hasattr(self, '_title'):
            self._title = get_object_or_404(
                Title, id=self.kwargs.get('title_id'))
        return self._title

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(title=title, author=self.request.user)

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PATCH']:
            return (IsModerOrReadOnly(),)
        return (IsAuthenticatedOrReadOnly(),)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        if not hasattr(self, '_review'):
            self._review = get_object_or_404(
                Review, id=self.kwargs.get('review_id'))
        return self._review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(review=review, author=self.request.user)

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PATCH']:
            return (IsModerOrReadOnly(),)
        return (IsAuthenticatedOrReadOnly(),)


class SignupView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
        )
        generate_confirmation_code(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Токен для подтверждения: {user.confirmation_code}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = generics.get_object_or_404(User, username=username)
        generate_confirmation_code(user)
        return Response(
            dict(token=str(AccessToken.for_user(user))),
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AdminOnly, )
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = (PageNumberPagination)

    @action(
            detail=False,
            methods=['get', 'patch'],
            url_path='me',
            permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            user = get_object_or_404(User, username=self.request.user.username)
            serializer = self.get_serializer(user, many=False)
            return Response(serializer.data)
        user = self.request.user
        serializer = MeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'me':
            return MeSerializer
        return UserSerializer
