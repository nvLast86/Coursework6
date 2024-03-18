import time
import smtplib
from datetime import datetime, timedelta
from django.db.models import F

from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from config.celery import app
from mailing.models import Mailing, MailingLogs



@app.task
def create_mailing(date_start, date_end, mailings_id, subject, body):
    now = datetime.now(timezone.utc)
    mailing_list = Mailing.objects.filter(time_start__lte=now)
    for mailing in mailing_list:
        subject = mailing.message.subject
        body = mailing.message.body

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()],
                fail_silently=False,
            )
            if mailing.frequency == '0':
                mailing.time_start = None
                mailing.status = 'completed'
            elif mailing.frequency == '1':
                mailing.time_start = F('sent_time') + timedelta(days=1)
                mailing.status = 'launched'
            elif mailing.frequency == '7':
                mailing.time_start = F('sent_time') + timedelta(days=7)
                mailing.status = 'launched'
            elif mailing.frequency == '30':
                mailing.time_start = F('sent_time') + timedelta(days=30)
                mailing.status = 'launched'
            mailing.save()

            try_status = 'SENT'
            server_response = 'успешно'
        except smtplib.SMTPResponseException as error:
            try_status = 'FAILED'
            server_response = str(error)

        finally:
            MailingLogs.objects.create(mailing=mailing, status=try_status, server_response=server_response, time=now)

