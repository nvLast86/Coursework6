from django.conf import settings
from django.core.cache import cache

from blog.models import Post


def cache_posts():
    """Кеширование всех постов"""
    data = Post.objects.all()
    if settings.CACHE_ENABLED:
        key = 'blog'
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = data
            cache.set(key, cache_data)
        return cache_data
    return data