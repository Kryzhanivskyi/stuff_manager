from django.core.management.base import BaseCommand, CommandError
from apps.account.models import User
import random
import names
import string


# generate random emails
domains = [ "hotmail.com", "gmail.com", "mail.com" , "mail.ru", "yahoo.com", "yandex.ru", "ukr.net"]
letters = string.ascii_lowercase[:12]

def get_one_random_domain(domains):
    return random.choice(domains)

def get_one_random_name(letters):
    return ''.join(random.choice(letters) for i in range(random.randint(5,12)))

def generate_random_emails():
    return get_one_random_name(letters) + '@' + get_one_random_domain(domains)


# TODO python manage.py create_test_data
class Command(BaseCommand):
    help = 'Create test data'

    def handle(self, *args, **options):
        print('User count', User.objects.count())
        print('hello from custom command')
        User.objects.exclude(is_superuser=True).delete()
        for i in range(10_000):
            user = User.objects.create(
                username=names.get_first_name() + names.get_last_name() + " " + names.get_first_name() + names.get_last_name(),
                first_name=names.get_first_name(),
                last_name=names.get_last_name(),
                email=generate_random_emails(),
                age=random.randint(18, 60),
                password=get_one_random_name(letters),
            )