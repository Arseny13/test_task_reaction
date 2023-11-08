from rest_framework import serializers

from .models import Blog


class BlogBaseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.username')

    class Meta:
        """Класс мета для модели Blog."""
        model = Blog
        fields = (
            'id',
            'name',
            'text',
            'publish',
            'user',
            'create_date'
        )


class BlogPostSerializer(BlogBaseSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )


class BlogUpdateSerializer(serializers.ModelSerializer):
    publish = serializers.BooleanField(required=True)

    class Meta:
        """Класс мета для модели Blog."""
        model = Blog
        fields = (
            'id',
            'name',
            'text',
            'publish',
        )
