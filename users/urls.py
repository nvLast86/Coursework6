from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users.views import ProfileUpdateView, RegisterView, generate_new_password, ActivateAccount

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/genpassword/', generate_new_password, name='generate_new_password'),
    path('activate/<uidb64>/<token>', ActivateAccount.as_view(), name='activate')
]
