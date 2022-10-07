from django.db import models


class Tags(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        unique=True,
        max_length=200
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код тега',
        unique=True,
        max_length=7
    )
    slug = models.SlugField(
        verbose_name='Идентификатор тега',
        unique=True,
        max_length=200
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
