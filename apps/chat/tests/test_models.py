from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.chat.models import Thread, Message

User = get_user_model()


class ThreadModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        self.thread = Thread.objects.create()

        self.thread.participants.add(self.user1, self.user2)

    def test_thread_creation(self):
        self.assertIsInstance(self.thread, Thread)
        self.assertEqual(str(self.thread), f"Thread {self.thread.id}")

    def test_thread_participants(self):
        self.assertIn(self.user1, self.thread.participants.all())
        self.assertIn(self.user2, self.thread.participants.all())

    def test_thread_str(self):
        self.assertEqual(str(self.thread), f"Thread {self.thread.id}")


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        self.thread = Thread.objects.create()
        self.thread.participants.add(self.user1, self.user2)

        self.message = Message.objects.create(
            sender=self.user1, text="Hello, this is a test message!", thread=self.thread
        )

    def test_message_creation(self):
        self.assertIsInstance(self.message, Message)
        self.assertEqual(self.message.text, "Hello, this is a test message!")
        self.assertEqual(self.message.sender, self.user1)
        self.assertEqual(self.message.thread, self.thread)

    def test_message_str(self):
        self.assertEqual(
            str(self.message), f"Message {self.message.id} from {self.message.sender}"
        )

    def test_message_is_read_default(self):
        self.assertFalse(self.message.is_read)
