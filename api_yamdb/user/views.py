from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from user.models import MyUser
from .serializers import (
    UserSerializer, EmailConfirmSerializer, TokenSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

  #  def get_permissions(self):
   #     if self.action == 'retrieve':
    #        return (ReadOnly(),)
     #   return super().get_permissions()


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


class TokenViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = TokenSerializer

    def get_token_for_user(self, serializer):
        if default_token_generator.check_token(
            self.request.user, serializer.data['confirmation_code']
        ):
            token = AccessToken.for_user(self.request.user)
            return {'access': str(token), }
