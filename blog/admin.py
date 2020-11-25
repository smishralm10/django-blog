from django.contrib import admin
from .models import Post, Comment

class CommentInLine(admin.TabularInline):
    model = Comment

class BlogAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine,
    ]



admin.site.register(Post, BlogAdmin)
admin.site.register(Comment)
