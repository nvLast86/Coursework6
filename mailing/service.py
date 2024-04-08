from django.conf import settings
from django.core.mail import send_mail


def send(header, contents, email):
    send_mail(
        subject=header,
        message=contents,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )