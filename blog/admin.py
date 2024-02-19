from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image', 'created_at', 'views_count',)
    search_fields = ('title', 'created_at', )
    list_filter = ('title', 'created_at', 'views_count',)
