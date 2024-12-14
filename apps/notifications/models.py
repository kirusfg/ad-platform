from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class NotificationType(models.Model):
    """
    Types of notifications that can be triggered
    e.g., "new_client", "event_reminder", "project_status_change"
    """

    code = models.CharField(_("Code"), max_length=100, unique=True)
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)

    # Default timeframe for reminders (in hours)
    default_remind_before = models.IntegerField(_("Default Remind Before (hours)"), default=24)

    class Meta:
        verbose_name = _("Notification Type")
        verbose_name_plural = _("Notification Types")

    def __str__(self):
        return self.name


class NotificationChannel(models.Model):
    """
    How the notification can be delivered
    """

    class Channel(models.TextChoices):
        EMAIL = "EMAIL", _("Email")
        SMS = "SMS", _("SMS")
        WEBSITE = "WEBSITE", _("Website")

    type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    channel = models.CharField(_("Channel"), max_length=20, choices=Channel.choices)
    template_subject = models.CharField(_("Template Subject"), max_length=255)
    template_body = models.TextField(_("Template Body"))

    class Meta:
        unique_together = ["type", "channel"]


class UserNotificationPreference(models.Model):
    """
    User preferences for notifications
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    email_enabled = models.BooleanField(_("Email Enabled"), default=True)
    sms_enabled = models.BooleanField(_("SMS Enabled"), default=False)
    website_enabled = models.BooleanField(_("Website Enabled"), default=True)
    remind_before = models.IntegerField(_("Remind Before (hours)"), null=True, blank=True, help_text=_("Override default reminder time"))

    class Meta:
        unique_together = ["user", "notification_type"]


class Notification(models.Model):
    """
    Actual notifications sent to users
    """

    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        SENT = "SENT", _("Sent")
        FAILED = "FAILED", _("Failed")
        READ = "READ", _("Read")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    channel = models.CharField(_("Channel"), max_length=20, choices=NotificationChannel.Channel.choices)
    title = models.CharField(_("Title"), max_length=255)
    message = models.TextField(_("Message"))
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    sent_at = models.DateTimeField(_("Sent At"), null=True, blank=True)
    error_message = models.TextField(_("Error Message"), blank=True)
    reference_object_type = models.CharField(_("Reference Object Type"), max_length=100, blank=True)
    reference_object_id = models.IntegerField(_("Reference Object ID"), null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
