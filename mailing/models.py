import datetime
from django.db import models
from config import settings
from users.models import NULLABLE


class Message(models.Model):
    header = models.CharField(max_length=150, verbose_name='тема')
    contents = models.TextField(verbose_name='содержание')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ('header',)

    def __str__(self):
        return self.header


class Contact(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    email = models.CharField(max_length=150, verbose_name='почта')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
        ordering = ('first_name',)

    def __str__(self):
        return self.email


class MailingLog(models.Model):
    time = models.DateTimeField(verbose_name='дата и время')
    attempt = models.BooleanField(default=True, verbose_name='статус попытки')
    server_response = models.BooleanField(default=True, verbose_name='ответ сервера')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
        ordering = ('server_response',)


class Mailing(models.Model):
    message = models.ForeignKey(Message, verbose_name='сообщение', on_delete=models.PROTECT)
    contacts = models.ManyToManyField(Contact, verbose_name='контакты')
    time = models.TimeField(verbose_name='время рассылки', default=datetime.time(8,00))
    last_sent = models.DateTimeField(verbose_name='время последней отправки', default=None, **NULLABLE)
    start_time = models.DateTimeField(verbose_name='дата и время начала рассылки в формате ДД.ММ.ГГГГ ЧЧ:ММ', default=None, **NULLABLE)
    finish_time = models.DateTimeField(verbose_name='дата и время окончания рассылки в формате ДД.ММ.ГГГГ ЧЧ:ММ', default=None, **NULLABLE)
    periods = (
        ('раз/день', 'раз/день'),
        ('раз/неделя', 'раз/неделя'),
        ('раз/месяц', 'раз/месяц'),
    )
    periodicity = models.CharField(choices=periods, verbose_name='периодичность')
    statuses = (
        ('завершена', 'завершена'),
        ('создана', 'создана'),
        ('запущена', 'запущена'),
    )
    status = models.CharField(choices=statuses, default='создана', verbose_name='статус рассылки')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    @property
    def emails(self):
        return ', '.join([contact.email for contact in self.contacts.all()])

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('status',)

