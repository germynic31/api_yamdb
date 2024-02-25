from user.models import MyUser
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),) #TODO сделаю в другой ветке
        return super().get_permissions()
