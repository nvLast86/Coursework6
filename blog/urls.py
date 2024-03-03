from django.urls import path

from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/<str:slug>/', PostDetailView.as_view(), name='post_detail')
]

