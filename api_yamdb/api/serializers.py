from rest_framework import serializers

from reviews.models import Title, Genre, Category
from .models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    title = serializers.SlugRelatedField(
        slug_field='id', many=False, read_only=True)

    class Meta:
        model = Review
        fields = ('title', 'text', 'author', 'score', 'pub_date', 'id')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    class CommentsSerializer(serializers.ModelSerializer):
        author = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='username'
        )
        review = serializers.SlugRelatedField(
            slug_field='text',
            many=False,
            read_only=True
        )

        class Meta:
            model = Comment
            fields = ('id', 'review', 'text', 'author', 'pub_date')


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

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class CreateUpdateDestroyTitleSerializer(serializers.ModelSerializer):
    """For create, update, destroy method."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='name',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
