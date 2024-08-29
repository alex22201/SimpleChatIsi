from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.chat.models import Message


@receiver(post_save, sender=Message)
def update_thread_on_message_save(sender, instance, **kwargs):
    thread = instance.thread
    thread.save()


@receiver(post_delete, sender=Message)
def update_thread_on_message_delete(sender, instance, **kwargs):
    thread = instance.thread
    thread.save()
