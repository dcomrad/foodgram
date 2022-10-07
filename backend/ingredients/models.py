from django.db import models


class Ingredients(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )

    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'

    class Meta:
        ordering = ['name', 'measurement_unit']
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
