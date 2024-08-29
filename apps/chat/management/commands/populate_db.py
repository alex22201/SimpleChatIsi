import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from apps.chat.models import Thread, Message

User = get_user_model()


class Command(BaseCommand):
    help = "Fills the database with test data"

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_users = 10
        num_threads = 10
        num_messages_per_thread = 100

        users = []
        for _ in range(num_users):
            user = User.objects.create(username=fake.user_name(), email=fake.email())
            users.append(user)

        for _ in range(num_threads):
            thread = Thread.objects.create()
            participants = fake.random_elements(elements=users, unique=True, length=2)
            thread.participants.set(participants)
            thread.save()

            for _ in range(num_messages_per_thread):
                sender = fake.random.choice(participants)
                Message.objects.create(
                    sender=sender,
                    thread=thread,
                    text=fake.text(),
                    created=fake.date_time_between(
                        start_date="-1y", end_date="now", tzinfo=datetime.timezone.utc
                    ),
                )

        self.stdout.write(
            self.style.SUCCESS(
                "The database has been successfully populated with test data."
            )
        )
