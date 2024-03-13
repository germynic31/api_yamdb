from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from reviews.models import User
from reviews import consts
from .mixins import ValidateUsernameMixin


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('title', 'text', 'author', 'score', 'pub_date', 'id')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data


class CommentsSerializer(serializers.ModelSerializer):
        author = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='username'
        )

        class Meta:
            model = Comment
            fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ListRetrieveTitleSerializer(serializers.ModelSerializer):
    """For list & retrieve method."""

    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    category = CategorySerializer(
        read_only=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class CreateUpdateDestroyTitleSerializer(serializers.ModelSerializer):
    """For create, update, destroy method."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class SignupSerializer(serializers.Serializer, ValidateUsernameMixin):
    email = serializers.EmailField(
        max_length=consts.EMAIL_LENGTH, required=True
    )
    username = serializers.CharField(
        max_length=consts.USERNAME_LENGTH, required=True
    )

    def validate(self, data):
        username = data['username']
        email = data['email']
        try:
            user_from_username = User.objects.get(username=username)
        except Exception:
            user_from_username = 1
        try:
            user_from_email = User.objects.get(email=email)
        except Exception:
            user_from_email = 1
        if user_from_username != user_from_email:
            raise serializers.ValidationError(
                'Нельзя использовать email или'
                'username существующего пользователя!'
            )
        return data


class TokenSerializer(serializers.Serializer, ValidateUsernameMixin):
    username = serializers.CharField(
        max_length=consts.USERNAME_LENGTH, required=True
    )
    confirmation_code = serializers.CharField(
        max_length=consts.CONFIRMATION_CODE_LENGTH, required=True
    )

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if data['confirmation_code'] != user.confirmation_code:
            raise serializers.ValidationError('Код подтверждения неверный!')


class UserSerializer(serializers.ModelSerializer, ValidateUsernameMixin):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class MeSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
