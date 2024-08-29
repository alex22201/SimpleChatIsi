from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.chat.models import Thread, Message, User


class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "testuser", "password": "password"},
            format="json",
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.user3 = User.objects.create(username="user3")


class ThreadViewsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.thread = Thread.objects.create()
        self.thread.participants.add(self.user1, self.user2)
        self.thread_url = reverse("thread-create")
        self.thread_delete_url = reverse("thread-delete", args=[self.thread.id])
        self.thread_list_url = reverse("thread-list", args=[self.user1.id])

    def test_create_thread(self):
        data = {"participants": [self.user1.id, self.user3.id]}
        response = self.client.post(self.thread_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Thread.objects.count(), 2)

    def test_existence_thread(self):
        data = {"participants": [self.user1.id, self.user2.id]}
        response = self.client.post(self.thread_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Thread.objects.count(), 1)

    def test_delete_thread(self):
        response = self.client.delete(self.thread_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Thread.objects.count(), 0)

    def test_list_threads(self):
        response = self.client.get(self.thread_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class MessageViewsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.thread = Thread.objects.create()
        self.thread.participants.add(self.user1, self.user2)
        self.message = Message.objects.create(
            sender=self.user1, text="Hello", thread=self.thread
        )
        self.message_create_url = reverse("message-create")
        self.message_list_url = reverse("message-list", args=[self.thread.id])
        self.message_mark_as_read_url = reverse(
            "message-mark-as-read", args=[self.message.id]
        )
        self.unread_message_count_url = reverse(
            "unread-message-count", args=[self.user1.id]
        )

    def test_create_message(self):
        data = {
            "sender": self.user1.id,
            "text": "Hello World",
            "thread": self.thread.id,
        }
        response = self.client.post(self.message_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)

    def test_list_messages(self):
        response = self.client.get(self.message_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_mark_message_as_read(self):
        response = self.client.patch(self.message_mark_as_read_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)

    def test_unread_message_count(self):
        response = self.client.get(self.unread_message_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["unread_count"], 1)
