from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, verification_user, display_verification, ProfileDeleteView, \
    UserListView, change_status_user

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/delete/<int:pk>', ProfileDeleteView.as_view(), name='profile_delete'),
    path('', display_verification, name='display_verification'),
    path('verification/<int:user_pk>/', verification_user, name='verification'),
    path('user/change-status/<int:user_pk>/', change_status_user, name='change_status')

]