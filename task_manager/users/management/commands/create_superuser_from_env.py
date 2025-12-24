import os
from django.core.management.base import BaseCommand
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from dotenv import load_dotenv
load_dotenv()


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_password = os.getenv('SUPERUSER')

        if not user_password:
            return

        user_password = user_password.split(':')
        user_name = user_password[0]
        password = user_password[1]

        User = get_user_model()
        if User.objects.filter(username=user_name).exists():
            print('SUPERUSER существует')
            return

        User.objects.create_superuser(user_name, password=password)
        print(f'Создан  {user_name}')


