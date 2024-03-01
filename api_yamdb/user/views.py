from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from user.models import MyUser
from .serializers import UserSerializer, EmailConfirmSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),) #TODO сделаю в другой ветке
        return super().get_permissions()


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


def get_token_for_user(user):
    token = AccessToken.for_user(user)
    return {'access': str(token), }
