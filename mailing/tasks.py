import time
from datetime import datetime

from dateutil import parser
from django.core.mail import send_mail
from django.utils import timezone

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path


from config import settings
from mailing.models import Mailing, MailingLogs


@app.task
def create_mailing(date_start, date_end, mailings_id, subject, body):
    mailing = Mailing.objects.get(id=mailings_id)
    date_start = parser.parse(str(date_start))
    date_end = parser.parse(str(date_end))
    while date_start <= timezone.now() <= date_end:
        try:
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [client.email for client in mailing.clients.all()],
            )
            MailingLogs.objects.create(
                time=timezone.now(),
                status='SENT',
                server_response='200',
                mailing=mailing,
            )
        except Exception:
            MailingLogs.objects.create(
                time=datetime.now(),
                status='FAILED',
                server_response='400',
                mailing=mailing,
            )

        time.sleep(Mailing.SLEEP_DICT[mailing.frequency])

    mailing.status = 'FINISHED'
    mailing.save()
    return 'mailings is finished'
