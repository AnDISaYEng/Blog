from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from posts.models import PostLike

User = get_user_model()


def add_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = PostLike.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)
    return like


def remove_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    PostLike.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()


def is_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    likes = PostLike.objects.filter(content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_likes_user(obj):
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(post_likes__content_type=obj_type, post_likes__object_id=obj.id)
