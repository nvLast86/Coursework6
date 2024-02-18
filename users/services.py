from django.core.mail import send_mail
from django.urls import reverse_lazy
from config import settings
from users.models import User


def send_code_email(user: User):
    """Отправляет ссылку для подтверждения почты"""
    send_mail(
        'Подтверждение почты',
        f'Чтобы подтвердить почту, перейдите по этой ссылке '\
        f'http://localhost:8000{reverse_lazy("users:verification", kwargs={"user_pk": user.pk})}',
        settings.EMAIL_HOST_USER,
        [user.email]
    )
