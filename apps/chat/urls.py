from django.urls import path
from .views import (
    ThreadCreateOrRetrieveView,
    MessageCreateView,
    MessageListView,
    MessageMarkAsReadView,
    UnreadMessageCountView,
    ThreadDeleteView,
    ThreadListView,
)

urlpatterns = [
    path("threads/", ThreadCreateOrRetrieveView.as_view(), name="thread-create"),
    path("threads/<int:thread_id>/", ThreadDeleteView.as_view(), name="thread-delete"),
    path("threads/list/<int:user_id>/", ThreadListView.as_view(), name="thread-list"),
    path("messages/", MessageCreateView.as_view(), name="message-create"),
    path("messages/<int:thread_id>/", MessageListView.as_view(), name="message-list"),
    path(
        "messages/<int:message_id>/mark_as_read/",
        MessageMarkAsReadView.as_view(),
        name="message-mark-as-read",
    ),
    path(
        "messages/unread_count/<int:user_id>/",
        UnreadMessageCountView.as_view(),
        name="unread-message-count",
    ),
]
