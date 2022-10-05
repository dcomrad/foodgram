from django.core.management.base import BaseCommand
import json
import os
from tags.models import Tags
from django.conf import settings


class Command(BaseCommand):
    FILEPATH = os.path.join(settings.BASE_DIR, '..', 'data', 'tags.json')

    def handle(self, *args, **options):
        with open(self.FILEPATH, 'rb') as file:
            message = 'Загрузка данных начата...'
            self.stdout.write(self.style.SUCCESS(message))
            tags = json.load(file)
            for tag in tags:
                Tags.objects.create(
                    name=tag['name'],
                    color=tag['color'],
                    slug=tag['slug'],
                )

        message = 'Список тэгов успешно загружены в базу данных'
        self.stdout.write(self.style.SUCCESS(message))
