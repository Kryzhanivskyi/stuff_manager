from uuid import uuid4
import random
from django.core.management.base import BaseCommand, CommandError
from apps.account.models import User, City


class Command(BaseCommand):
    help = 'Create test data'

    def handle(self, *args, **options):
        # https://pypi.org/project/names/
        User.objects.exclude(is_superuser=True).delete()
        result = []
        cities =[]
        for name in ("Kiev", "Odessa", "Lviv", "Dnipro"):
            city, _ = City.objects.get_or_create(name=name)
            cities.append(city)

        for i in range(10_000):
            username = str(uuid4())
            user = User(
                username=username,
                email=username + '@example.com',
                age=random.randint(12, 100),
                salary=random.randint(100, 1000),
                city=random.choice(cities),
            )
            result.append(user)
        User.objects.bulk_create(result)