import json
from django.utils import timezone
from datetime import timedelta

from celery import shared_task, Celery
from django.core.mail import send_mail
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from config import settings
from mailing.models import Mailing, MailingLog


app = Celery()

intervals = dict([
        ('раз/день', timedelta(days=1)),
        ('раз/неделя', timedelta(weeks=1)),
        ('раз/месяц', timedelta(days=30)),
])

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    schedule, created = IntervalSchedule\
        .objects.get_or_create(every=20, period=IntervalSchedule.MINUTES,)
    PeriodicTask.objects.get_or_create(interval=schedule, name='notifications.check_new_tasks',
                                       task='notifications.check_new_tasks',
                                       args=json.dumps(['every 20 minutes']),)


@app.task(bind=True, name='notifications.check_new_tasks')
def check_new_tasks(self, period="from db"):
    new_mailing_list = Mailing.objects.filter(status='создана')
    now = timezone.now()
    for mailing in new_mailing_list:
        if mailing.start_time and now > mailing.start_time:
            mailing.status = 'запущена'
            mailing.save()
    mailing_list = Mailing.objects.filter(status='запущена')
    for mailing in mailing_list:
        if mailing.finish_time and now > mailing.finish_time:
            mailing.status = 'завершена'
            mailing.save()
            continue
        delta = 0
        if mailing.last_sent:
            delta = now - mailing.last_sent
        time_delta = (now.hour * 60 + now.minute) - (mailing.time.hour * 60 + mailing.time.minute)
        its_send_time = now.hour == mailing.time.hour
        period = intervals[mailing.intervals]
        if (delta == 0 or delta > period) and time_delta > 0 and its_send_time:
            log = MailingLog(time=now, mailing=mailing)
            try:
                send_mail(
                    subject=mailing.message.header,
                    message=mailing.message.contents,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[contact.email for contact in mailing.contacts],
                    fail_silently=False,
                )
                mailing.last_sent = now
            except:
                log.attempt = False
                log.server_response = False
            log.save()
