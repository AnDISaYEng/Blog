from django.contrib import admin
from .models import Post, Tag, Comment, Favorites, PostLike

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Favorites)
admin.site.register(PostLike)

