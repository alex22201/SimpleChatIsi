from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.chat.models import Thread, Message, User
from apps.chat.serializers import (
    ThreadSerializer,
    MessageSerializer,
    MessageListSerializer,
    ThreadCreateOrRetrieveSerializer,
)
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import LimitOffsetPagination


@extend_schema(
    tags=["Threads"],
    request=ThreadCreateOrRetrieveSerializer,
)
class ThreadCreateOrRetrieveView(APIView):
    def post(self, request):
        serializer = ThreadCreateOrRetrieveSerializer(data=request.data)

        if serializer.is_valid():
            thread = serializer.save()
            thread_serializer = ThreadSerializer(thread)
            return Response(thread_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Threads"])
class ThreadDeleteView(APIView):
    def delete(self, request, thread_id: int):
        try:
            thread = Thread.objects.get(id=thread_id)
            thread.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Thread.DoesNotExist:
            return Response(
                {"error": "Thread not found."}, status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(tags=["Threads"])
class ThreadListView(APIView):
    def get(self, request, user_id: int):
        try:
            user = User.objects.get(id=user_id)
            threads = Thread.objects.filter(participants=user)

            # Apply pagination
            paginator = LimitOffsetPagination()
            result_page = paginator.paginate_queryset(threads, request)
            serializer = ThreadSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(tags=["Messages"], request=MessageSerializer)
class MessageCreateView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()

            thread = message.thread
            thread.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Messages"])
class MessageListView(APIView):
    def get(self, request, thread_id: int = None):
        if thread_id:
            messages = Message.objects.filter(thread=thread_id)
        else:
            messages = Message.objects.all()

        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(messages, request)
        serializer = MessageListSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)


@extend_schema(tags=["Messages"])
class MessageMarkAsReadView(APIView):
    def patch(self, request, message_id: int = None):
        try:
            message = Message.objects.get(id=message_id)
            message.is_read = True
            message.save()
            return Response({"status": "Message marked as read"})
        except Message.DoesNotExist:
            return Response(
                {"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(tags=["Messages"])
class UnreadMessageCountView(APIView):
    def get(self, request, user_id: int):
        user = User.objects.get(id=user_id)
        unread_count = Message.objects.filter(sender=user, is_read=False).count()
        return Response({"unread_count": unread_count})
