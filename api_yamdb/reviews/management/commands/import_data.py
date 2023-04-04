from csv import DictReader

from django.conf import settings
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

        for row in DictReader(
            open(settings.BASE_DIR / 'static' / 'data' / 'users.csv')
        ):
            user = User(
                id=row.get('id'),
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            user.save()
