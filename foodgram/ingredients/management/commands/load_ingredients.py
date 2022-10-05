from django.core.management.base import BaseCommand
import json
import os
from ingredients.models import Ingredients
from django.conf import settings


class Command(BaseCommand):
    FILEPATH = os.path.join(settings.BASE_DIR, '..', 'data', 'ingredients.json')

    def handle(self, *args, **options):
        with open(self.FILEPATH, 'rb') as file:
            message = 'Загрузка данных начата...'
            self.stdout.write(self.style.SUCCESS(message))
            ingredients = json.load(file)
            for ingredient in ingredients:
                Ingredients.objects.create(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit']
                )

        message = 'Список ингредиентов успешно загружены в базу данных'
        self.stdout.write(self.style.SUCCESS(message))
