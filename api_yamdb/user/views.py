from django.core.mail import send_mail
from rest_framework import filters, generics, status, views, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from user.models import MyUser
from .permissions import AdminOnly
from .serializers import (
    MeSerializer, SignupSerializer, TokenSerializer, UserSerializer
)
from .utils import check_confirmation_code, generate_confirmation_code


class SignupView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, created = MyUser.objects.get_or_create(
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
        user = generics.get_object_or_404(MyUser, username=username)
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
    queryset = MyUser.objects.all()
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
