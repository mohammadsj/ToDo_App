from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from todo.models import Task


class Command(BaseCommand):
    help = "Generates fake users and categories and posts"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):

        user = User.objects.create_user(
            username=self.fake.user_name(),
            email=self.fake.email(),
            password=self.fake.password(length=12),
        )
        for _ in range(5):
            Task.objects.create(
                user=user, title=self.fake.catch_phrase(), complete=self.fake.boolean()
            )
