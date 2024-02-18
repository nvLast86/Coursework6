import time
from datetime import datetime

from dateutil import parser
from django.core.mail import send_mail
from django.utils import timezone

from config.celery import app
from config import settings
from mailing.models import Mailing, MailingsLogs


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
            MailingsLogs.objects.create(
                time=timezone.now(),
                status='SENT',
                server_response='200',
                mailing=mailing,
            )
        except Exception:
            MailingsLogs.objects.create(
                time=datetime.now(),
                status='FAILED',
                server_response='400',
                mailing=mailing,
            )

        time.sleep(Mailings.SLEEP_DICT[mailing.frequency])

    mailing.status = 'FINISHED'
    mailing.save()
    return 'mailings is finished'
