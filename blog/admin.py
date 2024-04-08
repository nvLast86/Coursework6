from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'contents')
    search_fields = ('name', 'contents')
    list_filter = ('contents',)
    prepopulated_fields = {"slug": ("name",)}

