import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from tags.models import Tags


class Command(BaseCommand):
    FILEPATH = os.path.join(settings.BASE_DIR, 'data', 'tags.json')

    def handle(self, *args, **options):
        with open(self.FILEPATH, 'rb') as file:
            try:
                message = 'Загрузка данных начата...'
                self.stdout.write(self.style.SUCCESS(message))
                tags = json.load(file)
                tags_obj = list(
                    Tags(
                        name=tag['name'],
                        color=tag['color'],
                        slug=tag['slug']
                    ) for tag in tags
                )
                Tags.objects.bulk_create(tags_obj)
                message = 'Список тэгов успешно загружены в базу данных'
                self.stdout.write(self.style.SUCCESS(message))
            except Exception as ex:
                message = f'Ошибка загрузки тэгов в базу данных: {ex}'
                self.stdout.write(self.style.SUCCESS(message))
