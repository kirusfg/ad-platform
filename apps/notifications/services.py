from django.template import Template, Context
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Q

import requests
from datetime import timedelta

from .models import NotificationType, NotificationChannel, UserNotificationPreference, Notification

User = get_user_model()


class NotificationService:
    @classmethod
    def create_notification(cls, notification_type_code, user, context_data, reference_object=None):
        """
        Create notifications based on user preferences
        """
        try:
            notification_type = NotificationType.objects.get(code=notification_type_code)
            preferences = UserNotificationPreference.objects.get(user=user, notification_type=notification_type)

            channels = NotificationChannel.objects.filter(type=notification_type)

            for channel in channels:
                if getattr(preferences, f"{channel.channel.lower()}_enabled", False):
                    # Render templates
                    subject_template = Template(channel.template_subject)
                    body_template = Template(channel.template_body)
                    context = Context(context_data)

                    title = subject_template.render(context)
                    message = body_template.render(context)

                    # Create notification
                    notification = Notification.objects.create(
                        user=user,
                        notification_type=notification_type,
                        channel=channel.channel,
                        title=title,
                        message=message,
                        status="PENDING",
                        reference_object_type=reference_object.__class__.__name__ if reference_object else "",
                        reference_object_id=reference_object.id if reference_object else None,
                    )

                    # Send notification immediately
                    cls.send_notification(notification)

        except (NotificationType.DoesNotExist, UserNotificationPreference.DoesNotExist):
            pass

    @classmethod
    def send_notification(cls, notification):
        """
        Send notification through appropriate channel
        """
        try:
            if notification.channel == "EMAIL":
                cls._send_email(notification)
            elif notification.channel == "SMS":
                cls._send_sms(notification)
            elif notification.channel == "WEBSITE":
                cls._send_website(notification)

            notification.status = "SENT"
            notification.sent_at = timezone.now()
            notification.save()

        except Exception as e:
            notification.status = "FAILED"
            notification.error_message = str(e)
            notification.save()

    @classmethod
    def _send_email(cls, notification):
        # Implement email sending logic
        pass

    @classmethod
    def _send_sms(cls, notification):
        # Implement SMS sending logic
        pass

    @classmethod
    def _send_website(cls, notification):
        # Website notifications are created but not "sent"
        notification.status = "SENT"
        notification.save()

    @classmethod
    def process_event_reminders(cls):
        """
        Process event reminders
        """
        now = timezone.now()
        notification_type = NotificationType.objects.get(code="event_reminder")

        # Get all upcoming events
        from apps.events.models import Event

        upcoming_events = Event.objects.filter(
            start_datetime__gt=now,
            start_datetime__lte=now + timedelta(days=7),  # Look ahead 7 days
        )

        for event in upcoming_events:
            # Get users who should be notified
            preferences = UserNotificationPreference.objects.filter(notification_type=notification_type)

            for pref in preferences:
                remind_before = pref.remind_before or notification_type.default_remind_before
                remind_at = event.start_datetime - timedelta(hours=remind_before)

                if now >= remind_at:
                    # Create notification
                    cls.create_notification(
                        "event_reminder", pref.user, {"event": event, "hours_until": remind_before}, reference_object=event
                    )
