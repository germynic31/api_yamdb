from api.mixins import ValidateUsernameMixin
from rest_framework import serializers
from user.models import MyUser


class SignupSerializer(serializers.Serializer, ValidateUsernameMixin):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)


class TokenSerializer(serializers.Serializer, ValidateUsernameMixin):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=6, required=True)


class UserSerializer(serializers.ModelSerializer, ValidateUsernameMixin):

    class Meta:
        model = MyUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class MeSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
