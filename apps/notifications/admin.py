from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import NotificationType, NotificationChannel, UserNotificationPreference, Notification


@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "default_remind_before", "get_channels")
    search_fields = ("name", "code", "description")
    ordering = ("name",)

    def get_channels(self, obj):
        channels = NotificationChannel.objects.filter(type=obj)
        return ", ".join([c.get_channel_display() for c in channels])

    get_channels.short_description = _("Available Channels")


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):
    list_display = ("type", "channel", "template_subject")
    list_filter = ("type", "channel")
    search_fields = ("template_subject", "template_body")

    fieldsets = (
        (None, {"fields": ("type", "channel")}),
        (
            _("Templates"),
            {
                "fields": ("template_subject", "template_body"),
                "description": format_html(
                    """
                <div class="help">
                    <p>Available variables:</p>
                    <ul>
                        <li><code>{{ user.name }}</code> - Recipient's name</li>
                        <li><code>{{ user.email }}</code> - Recipient's email</li>
                        <li><code>{{ event.title }}</code> - Event title (for event notifications)</li>
                        <li><code>{{ event.start_datetime }}</code> - Event start time</li>
                        <li><code>{{ project.name }}</code> - Project name</li>
                        <li><code>{{ project.status }}</code> - Project status</li>
                        <li><code>{{ client.name }}</code> - Client name</li>
                        <li><code>{{ hours_until }}</code> - Hours until event (for reminders)</li>
                    </ul>
                </div>
                """
                ),
            },
        ),
    )


@admin.register(UserNotificationPreference)
class UserNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "notification_type", "email_enabled", "sms_enabled", "website_enabled", "remind_before")
    list_filter = ("notification_type", "email_enabled", "sms_enabled", "website_enabled")
    search_fields = ("user__username", "user__email", "notification_type__name")
    raw_id_fields = ("user",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "notification_type", "channel", "title", "status", "created_at", "sent_at")
    list_filter = ("status", "channel", "notification_type", "created_at", "sent_at")
    search_fields = ("user__username", "user__email", "title", "message")
    raw_id_fields = ("user",)
    readonly_fields = ("created_at", "sent_at", "error_message")

    fieldsets = (
        (None, {"fields": ("user", "notification_type", "channel", "status")}),
        (_("Content"), {"fields": ("title", "message")}),
        (_("Reference"), {"fields": ("reference_object_type", "reference_object_id")}),
        (_("Timing"), {"fields": ("created_at", "sent_at")}),
        (_("Error Details"), {"fields": ("error_message",), "classes": ("collapse",)}),
    )

    def has_add_permission(self, request):
        return False  # Notifications should only be created through the service
