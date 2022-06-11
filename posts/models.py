from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class PostLike(models.Model):
    user = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='post_likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tag = models.ForeignKey(Tag,
                            on_delete=models.RESTRICT,
                            related_name='posts')
    image = models.ImageField(upload_to='posts',
                              null=True,
                              blank=True)
    likes = GenericRelation(PostLike)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # default=datetime.now(), blank=True

    def __str__(self):
        return f'{self.post}  ---  {self.text}'



class Favorites(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorites',
                             default='')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='favorites')

    def __str__(self):
        return '{0}'.format(self.post)
