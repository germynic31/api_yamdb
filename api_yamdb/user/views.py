from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets, views
from rest_framework.permissions import IsAdminUser
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
from utils import generate_confirmation_code, check_confirmation_code


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

    #  def get_permissions(self):
    #     if self.action == 'retrieve':
    #        return (ReadOnly(),)
    #   return super().get_permissions()


class SignupView(views.APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, created = MyUser.objects.get_or_create(
                username=username,
                email=email,
            )
        except Exception:
            return Response(
                dict[('error', 'Username или email уже есть в системе.'),],
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = generate_confirmation_code(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Токен для подтверждения: {confirmation_code}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailViewSet(viewsets.GenericViewSet):
    queryset = MyUser.objects.all()
    serializer_class = EmailConfirmSerializer

    @action(methods=['post'], detail=False, url_path='signup')
    def mail(self, serializer):
        logging.info('зашёл в мэйл')
        try:
            user = MyUser.objects.get(username=serializer.data['username'])
        except Exception:
            user = MyUser.objects.create(
                username=serializer.data['username'],
                email=serializer.data['email'],
            )
        logging.info(user)
        token = user.confirmation_code
        logging.info(token)
        send_mail(
            subject='Код подтверждения',
            message=f'Токен для подтверждения: {token}',
            from_email='from@example.com',
            recipient_list=[serializer.data['email']],
            fail_silently=True,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class TokenViewSet(viewsets.GenericViewSet):
    queryset = MyUser.objects.all()
    serializer_class = TokenSerializer

    @action(methods=['post'], detail=False, url_path='token')
    def get_token_for_user(self, serializer):
        if default_token_generator.check_token(
            MyUser.objects.get(username=serializer.data['username']),
            serializer.data['confirmation_code']
        ):
            token = AccessToken.for_user(MyUser.objects.get(username=serializer.data['username']))
            headers = self.get_success_headers(serializer.data)
            return Response(
                {'access': str(token), },
                status=status.HTTP_200_OK,
                headers=headers
            )

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
