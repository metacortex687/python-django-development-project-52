import os
from django.core.management.base import BaseCommand, CommandError
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model 

from dotenv import load_dotenv
load_dotenv()


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_name = os.getenv('SUPERUSER').split(':')[0]
        password = os.getenv('SUPERUSER').split(':')[1]
        
        User = get_user_model()
        if User.objects.filter(username=user_name).exists():
            print('SUPERUSER существует')
            return
        
        User.objects.create_superuser(user_name, password=password)

       
