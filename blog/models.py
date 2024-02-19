from django.db import models
from pytils.translit import slugify

from mailing.models import NULLABLE


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    content = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to='posts/', verbose_name='изображение', **NULLABLE)
    created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    views_count = models.PositiveIntegerField(verbose_name='количество просмотров', default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.slug is None:
            self.slug = slugify(self.title)

    def __str__(self):
        return f'{self.title} {self.slug}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created_at',)

    def increase_views_count(self):
        """
        Увеличивает просмотры поста на 1.
        """
        self.views_count += 1
        self.save()
