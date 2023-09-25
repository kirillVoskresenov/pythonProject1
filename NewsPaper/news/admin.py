from django.contrib import admin
from .models import Author, Post, Category, Comment, PostCategory


admin.site.register(Post)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Category)