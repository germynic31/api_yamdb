from rest_framework import serializers

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
