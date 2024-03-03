from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import AccessToken
from user.models import MyUser
from .serializers import (
    UserSerializer, EmailConfirmSerializer, TokenSerializer
)
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings


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


class EmailViewSet(viewsets.GenericViewSet):
    queryset = MyUser.objects.all()
    serializer_class = EmailConfirmSerializer

    @action(methods=['post'], detail=False, url_path='signup')
    def mail(self, serializer):
        logging.info('зашёл в мэйл')
        user = MyUser.objects.get(username=serializer.data['username'])
        logging.info(user)
        token = default_token_generator.make_token(user)
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
