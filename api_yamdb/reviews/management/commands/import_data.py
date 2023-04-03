from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import User

ALREADY_LOADED_ERROR_MESSAGE = '''
    Данные уже загружены.
'''


class Command(BaseCommand):
    help = 'Описание для работы с командой.'

    def handle(self, *args, **options) -> None:
        if User.objects.exists():
            print('Данные о пользователе уже загружены.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        print('Загружаем данные.')

        for row in DictReader(open()):
            ...
