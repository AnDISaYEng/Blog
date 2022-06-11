from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from posts import likes_services
from posts.filter import PostFilter
from posts.models import Post, Tag, Comment, Favorites, PostLike
from posts.permissions import IsAdmin, IsAuthor
from posts.serializers import PostSerializer, TagSerializer, CommentSerializer, FavoritesGetSerializer, \
    FavoritesCreateSerializer, FavoritesDestroySerializer, \
    FanSerializer


class LikedMixin:
    @action(['POST'], detail=True)
    def like(self, request, pk):
        post = self.get_object()
        likes_services.add_like(post, request.user)
        return Response()

    @action(['POST'], detail=True)
    def unlike(self, request, pk):
        post = self.get_object()
        likes_services.remove_like(post, request.user)
        return Response()

    @action(['GET'], detail=True)
    def likes(self, request, pk):
        post = self.get_object()
        likes = likes_services.get_likes_user(post)
        serializer = FanSerializer(likes, many=True)
        return Response(serializer.data)


class PostViewSet(LikedMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = PostFilter
    search_fields = ['title']

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(['GET'], detail=True)
    def post_like(self, request, pk):
        post = self.get_object()
        post_likes = post.post_likes.all()
        serializer = PostLikeSerializer(post_likes, many=True)
        return Response(serializer.data)

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return []
    #     if self.action == 'create':
    #         return [IsAuthenticated()]
    #     if self.action == 'destroy':
    #         return [IsAdmin()]
    #     if self.action == 'update':
    #         return [IsAuthor()]


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdmin]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action == 'list':
            return []
        return [IsAuthor()]


class FavoritesListView(ListAPIView):
    queryset = Favorites.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesGetSerializer

    def get(self, request):
        data = request.data
        serializer = FavoritesGetSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class FavoritesCreateView(CreateAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesCreateSerializer


class FavoritesDestroyView(DestroyAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesDestroySerializer
