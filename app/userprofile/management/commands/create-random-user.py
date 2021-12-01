import string

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):
    help = "generate fake random user"

    def handle(self, *args, **options):
        total = 10
        for i in range(total):
            username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
            email = '{}@wownet.id'.format(username)
            password = get_random_string(50)
            User.objects.create_user(username=username, email=email, password=password)
        return '{} raaandom users created succesfully'.format(total)


