from django.views.generic import ListView, DetailView

from blog.models import Post
from blog.services import cache_posts


class PostListView(ListView):
    model = Post
    data = Post.objects.all()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['subjects'] = cache_posts()
        return context_data


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.increase_views_count()
        return post

