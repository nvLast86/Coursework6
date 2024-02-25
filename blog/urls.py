from django.urls import path

from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/<str:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('posts/update/<slug:slug>/', PostUpdateView.as_view(), name='post_update'),
    path('posts/delete/<slug:slug>/', PostDeleteView.as_view(), name='post_delete'),
]

