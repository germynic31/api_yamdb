from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets, views
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from user.models import MyUser
from .serializers import (
    UserSerializer, SignupSerializer, TokenSerializer
)
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings
from .utils import generate_confirmation_code, check_confirmation_code


import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w'
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

    #def get_permissions(self):
    #    if self.action == 'retrieve':
    #        return (ReadOnly(),)
    #    return super().get_permissions()


class SignupView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        logging.info('зашёл в пост')
        serializer = SignupSerializer(data=request.data)
        logging.info('выбрал сериалайзер')
        serializer.is_valid(raise_exception=True)
        logging.info('валидация')
        username = serializer.validated_data.get('username')
        logging.info('имя')
        email = serializer.validated_data.get('email')
        logging.info('мэйл')
        try:
            logging.info('зашёл в трай')
            user, created = MyUser.objects.get_or_create(
                username=username,
                email=email,
            )
            logging.info(user)
        except Exception:
            return Response(
                dict[('error', 'Username или email уже есть в системе.'),],
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = generate_confirmation_code(user)
        logging.info(confirmation_code)
        send_mail(
            subject='Код подтверждения',
            message=f'Токен для подтверждения: {confirmation_code}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = MyUser.objects.get(username=username)
        if check_confirmation_code(user, confirmation_code):
            return Response(
                dict[('token', AccessToken.for_user(user)),],
                status=status.HTTP_200_OK
            )
        return Response(
            dict[('error', 'Ошибка кода подтверждения.'),],
            status=status.HTTP_400_BAD_REQUEST
        )
