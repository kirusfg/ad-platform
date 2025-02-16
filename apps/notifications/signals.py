from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.projects.models import Project
from apps.channels.models import Channel

from .models import Notification
from .utils import send_email_notification, send_whatsapp_notification

User = get_user_model()


@receiver(post_save, sender=Project)
def project_created_notification(sender, instance, created, **kwargs):
    if created:
        User = get_user_model()
        creator = getattr(instance, "created_by", None)
        # Notify all users except the creator (if defined)
        users_to_notify = User.objects.exclude(pk=creator.pk) if creator else User.objects.all()
        for user in users_to_notify:
            Notification.objects.create(user=user, message=_("New project %(name)s created") % {"name": instance.name})


@receiver(post_save, sender=Channel)
def channel_status_changed_notification(sender, instance, created, **kwargs):
    if not created:
        # Assuming each project has a ForeignKey to Channel named 'channel'
        from apps.projects.models import Project

        # Gather users with projects using this channel
        projects = Project.objects.filter(channels=instance)
        users_to_notify = set(getattr(project, "created_by", None) for project in projects if getattr(project, "created_by", None))
        for user in users_to_notify:
            Notification.objects.create(
                user=user,
                message=_("Channel %(name)s status changed to %(status)s")
                % {"name": instance.name, "status": instance.get_status_display()},
            )


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created and not settings.NO_NOTIFICATIONS:
        user = instance.user
        subject = _("AdSphere - New Notification")
        message = instance.message

        if user.email and user.email.endswith("@gmail.com"):
            send_email_notification(subject, message, [user.email])

        if user.phone_number and user.phone_number.startswith("+7"):
            send_whatsapp_notification(message, user.phone_number)
