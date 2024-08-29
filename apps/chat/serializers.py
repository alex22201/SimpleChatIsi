from django.db.models import Count
from rest_framework import serializers
from .models import Thread, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class ThreadCreateOrRetrieveSerializer(serializers.Serializer):
    participants = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=2,
        max_length=2,
        error_messages={
            "min_length": "Thread must have exactly two participants.",
            "max_length": "Thread must have exactly two participants.",
        },
    )

    def validate_participants(self, participants_ids):
        participants = User.objects.filter(id__in=participants_ids)
        if len(participants) != 2:
            raise serializers.ValidationError("One or both participants do not exist.")
        return participants

    def create(self, validated_data):
        participants = validated_data["participants"]
        participants_ids = set(participants.values_list("id", flat=True))

        # Find threads with exact matching participants
        existing_threads = (
            Thread.objects.filter(participants__in=participants)
            .annotate(num_participants=Count("participants"))
            .filter(num_participants=2)
            .distinct()
        )

        for thread in existing_threads:
            if (
                set(thread.participants.values_list("id", flat=True))
                == participants_ids
            ):
                return thread

        thread = Thread.objects.create()
        thread.participants.set(participants)
        thread.save()
        return thread


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )

    class Meta:
        model = Thread
        fields = ["id", "participants", "created", "updated"]


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all())

    class Meta:
        model = Message
        fields = ["id", "sender", "text", "thread", "created"]


class MessageListSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ["id", "sender", "text", "created", "is_read"]
