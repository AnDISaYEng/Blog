from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (PostViewSet, TagViewSet,
                    CommentViewSet, FavoritesListView, FavoritesCreateView, FavoritesDestroyView)


router = SimpleRouter()
router.register('post', PostViewSet)
router.register('tags', TagViewSet)
router.register('comments', CommentViewSet)
# router.register('favorites_list', FavoritesListView)
# router.register('post_likes', LikeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('favorites/', FavoritesListView.as_view()),
    path('favorites/add/', FavoritesCreateView.as_view()),
    path('favorites/delete/<int:pk>/', FavoritesDestroyView.as_view()),
    # path('post/<int:pk>/add/', LikeCreateView.as_view()),
    # path('post/<int:pk>/remove/', LikeDestroyView.as_view()),

]
