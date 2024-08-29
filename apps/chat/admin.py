from django.contrib import admin
from django.utils import timezone

from .models import Thread, Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "updated")
    filter_horizontal = ("participants",)
    search_fields = ("id",)
    ordering = ("-created",)

    fieldsets = (
        (None, {"fields": ("participants",)}),
        ("Dates", {"fields": ("created", "updated"), "classes": ("collapse",)}),
    )

    readonly_fields = ("created", "updated")

    actions = ["mark_as_updated"]

    def mark_as_updated(self, request, queryset):
        rows_updated = queryset.update(updated=timezone.now())
        self.message_user(request, f"{rows_updated} threads updated.")

    mark_as_updated.short_description = "Mark selected threads as updated"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "thread", "created", "is_read")
    list_filter = ("is_read", "thread")
    search_fields = ("text", "sender__username")
    ordering = ("-created",)

    fieldsets = (
        (None, {"fields": ("sender", "thread", "text", "is_read")}),
        ("Dates", {"fields": ("created",), "classes": ("collapse",)}),
    )

    readonly_fields = ("created",)

    actions = ["mark_all_as_read"]

    def mark_all_as_read(self, request, queryset):
        rows_updated = queryset.update(is_read=True)
        self.message_user(request, f"{rows_updated} messages marked as read.")

    mark_all_as_read.short_description = "Mark selected messages as read"
