from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts import likes_services
from posts.models import Post, Tag, Comment, Favorites, PostLike

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'is_like', 'total_likes', 'image', 'created_at', 'tag']

    def get_is_like(self, post):
        user = self.context.get('request').user
        return likes_services.is_like(post, user)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'text', 'rating', 'created_at']

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 5')
        return rating

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)


class FavoritesGetSerializer(serializers.Serializer):
    user = serializers.EmailField(required=True)

    def validate_user(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate(self, attrs):
        user = attrs.get('user')
        favorites_queryset = Favorites.objects.filter(user=user)
        favorites_queryset = [favorites_queryset[i] for i in range(len(favorites_queryset))]
        favorites = [str(favorites_queryset[i]) for i in range(len(favorites_queryset))]
        attrs['user'] = favorites
        return attrs


class FavoritesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate_post(self, post):
        if not Post.objects.filter(title=post).exists():
            raise serializers.ValidationError('Такого поста не существует')
        return post

    def validate(self, attrs):
        user = attrs.get('user')
        post = attrs.get('post')
        favorites_queryset = Favorites.objects.filter(user=user)
        favorites_queryset = [favorites_queryset[i] for i in range(len(favorites_queryset))]
        favorites = [str(favorites_queryset[i]) for i in range(len(favorites_queryset))]
        if str(post) in favorites:
            raise serializers.ValidationError('Вы уже добавили пост в избранное')
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)


class FavoritesDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'


class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
