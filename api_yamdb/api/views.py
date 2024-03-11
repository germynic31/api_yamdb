from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, views, viewsets
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
from reviews.utils import check_confirmation_code, generate_confirmation_code
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


class SignupView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, created = User.objects.get_or_create(
                username=username,
                email=email,
            )
        except Exception:
            return Response(
                dict(error='Username или email уже есть в системе.'),
                status=status.HTTP_400_BAD_REQUEST
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
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = generics.get_object_or_404(User, username=username)
        if check_confirmation_code(user, confirmation_code):
            return Response(
                dict(token=str(AccessToken.for_user(user))),
                status=status.HTTP_200_OK
            )
        return Response(
            dict(error='Ошибка кода подтверждения.'),
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly, )
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = (PageNumberPagination)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = MeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
