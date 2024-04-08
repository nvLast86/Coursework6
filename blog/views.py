from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic

from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(generic.ListView):
    model = Blog


class BlogDetailView(generic.DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data

    def get_object(self, **kwargs):
        views = super().get_object()
        views.increase_view_count()
        return views


class BlogCreateView(PermissionRequiredMixin, generic.CreateView):
    model = Blog
    permission_required = "blog.add_blog"
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Blog
    permission_required = "blog.change_blog"
    fields = ('name', 'contents', 'preview', 'published')

    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.object.slug})


class BlogDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Blog
    permission_required = "blog.delete_blog"
    success_url = reverse_lazy('catalog:blog_list')
