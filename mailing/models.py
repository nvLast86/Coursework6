from django.db import models
from config import settings
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Модель, описывающая клиента"""

    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f'{self.name} - {self.email}'


class Message(models.Model):
    """Модель, описывающая тему и сообщение рассылки"""
    subject = models.TextField(verbose_name='тема письма')
    body = models.TextField(verbose_name='текст письма')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    """Модель, описывающая настройки рассылки"""
    FREQUENCY_CHOICES = [
        ('DAILY', 'Раз в день'),
        ('WEEKLY', 'Раз в неделю'),
        ('MONTHLY', 'Раз в месяц')
    ]
    SLEEP_DICT = {
        'DAILY': 20,
        'WEEKLY': 30,
        'MONTHLY': 60
    }

    STATUS_CHOICES = [
        ('CREATED', 'Создана'),
        ('STARTED', 'Запущена'),
        ('FINISHED', 'Завершена')
    ]

    time_start = models.DateTimeField(verbose_name='время начала рассылки')
    time_end = models.DateTimeField(verbose_name='время конца рассылки')
    frequency = models.TextField(max_length=10, verbose_name='периодичность', choices=FREQUENCY_CHOICES)
    status = models.TextField(max_length=10, verbose_name='статус', choices=STATUS_CHOICES, default='CREATED')

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='тема письма')
    clients = models.ManyToManyField(Client, verbose_name='клиенты')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def __str__(self):
        return f'Рассылка {self.pk}'


class MailingLogs(models.Model):
    """Модель, описывающая логи рассылки"""

    STATUS_CHOICES = [
        ('SENT', 'Отправлено'),
        ('FAILED', 'Не удалось отправить'),
    ]

    time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время попытки')
    status = models.TextField(verbose_name='статус попытки', choices=STATUS_CHOICES)
    server_response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)

    mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, verbose_name='рассылка')

    class Meta:
        verbose_name = 'лог отправки письма'
        verbose_name_plural = 'логи отправки писем'

    def __str__(self):
        return f'Лог {self.pk}'

