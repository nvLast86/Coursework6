import random
from time import time

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView, CreateView, View
from users.models import User
from users.forms import UserForm, UserRegisterForm
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.contrib.auth import login

from users.tokens import account_activation_token


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/user_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Активируйте ваш аккаунт'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            with open(settings.TEMP_EMAIL_DIR / '{}.html'.format(time()), 'w') as f:
                f.write(message)
            # user.email_user(subject, message)

            messages.success(request, ('Пожалуйста, перейдите по ссылке, чтобы закончить регистрацию.'))

            return redirect('users:login')

        return render(request, self.template_name, {'form': form})



def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(15)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('mailing:home'))


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_verify = True
            user.save()
            login(request, user)
            messages.success(request, ('Ваш аккаунт подтвержден.'))
            return redirect('mailing:home')
        else:
            messages.warning(request, ('Ссылка для подтверждения недействительна.'))
            return redirect('mailing:home')
