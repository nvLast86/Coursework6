from django.db import models
from django.urls import reverse
from pytils.translit import slugify

from users.models import NULLABLE


class Blog(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='URl')
    contents = models.TextField(verbose_name='содержание')
    creation_date = models.DateField(auto_now_add=True, verbose_name='дата создания')
    preview = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    published = models.DateField(verbose_name='дата публикации')
    views_number = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def increase_view_count(self):
        self.views_number += 1
        self.save()

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        ordering = ('name',)
