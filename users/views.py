from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from users.services import send_code_email
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserListView(ListView):
    model = User

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:display_verification')

    def form_valid(self, form):
        obj = form.save()
        obj.is_active = False
        obj.save()
        send_code_email(obj)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailings:home')

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:register')


def display_verification(request):
    """Перенаправляет на сообщение о верификации"""
    return render(request, 'users/verification.html')


def verification_user(request, user_pk):
    """Верификация почты, после прохождения по ссылке перенаправляет на личные данные"""
    user = get_object_or_404(User, pk=user_pk)
    user.is_active = True
    user.save()
    login(request, user)
    return redirect(reverse('users:profile'))


def change_status_user(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse('users:user_list'))

