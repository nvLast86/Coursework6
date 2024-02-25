from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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


class PostCreateView(CreateView):
    model = Post
    fields = ('title', 'content', 'image',)
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'content', 'image',)

    def get_success_url(self):
        return reverse('blog:post_list', args=[self.object.slug])


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
