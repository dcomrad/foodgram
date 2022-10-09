import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from ingredients.models import Ingredients


class Command(BaseCommand):
    FILEPATH = os.path.join(settings.BASE_DIR, 'data', 'ingredients.json')

    def handle(self, *args, **options):
        with open(self.FILEPATH, 'rb') as file:
            try:
                message = 'Загрузка данных начата...'
                self.stdout.write(self.style.SUCCESS(message))
                ingredients = json.load(file)
                ingredients_obj = list(
                    Ingredients(
                        name=ingredient['name'],
                        measurement_unit=ingredient['measurement_unit']
                    ) for ingredient in ingredients
                )
                Ingredients.objects.bulk_create(ingredients_obj)
                message = 'Список ингредиентов успешно загружены в базу данных'
                self.stdout.write(self.style.SUCCESS(message))
            except Exception as ex:
                message = f'Ошибка загрузки ингредиентов в базу данных: {ex}'
                self.stdout.write(self.style.SUCCESS(message))
