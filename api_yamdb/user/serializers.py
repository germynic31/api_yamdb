from rest_framework import serializers

from user.models import MyUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        extra_kwargs = {
            'username': {'unique': True, 'required': True},
            'email': {'unique': True, 'required': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        user = MyUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            bio=validated_data['bio'],
            role=validated_data['role']
        )
        user.save()
        return user


class EmailConfirmSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('email', 'username')

    def validate_username(self, value):
        if 'me' == value:
            raise serializers.ValidationError(
                'Нельзя использовать username "me"!')
        return value


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField()

    class Meta:
        model = MyUser
        fields = ('username', 'confirmation_code')
