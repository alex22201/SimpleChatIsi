from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


class Thread(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="threads"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"Thread {self.id}"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(
        Thread, related_name="messages", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return f"Message {self.id} from {self.sender}"


User = get_user_model()
