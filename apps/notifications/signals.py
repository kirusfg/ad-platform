from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.clients.models import Client
from apps.projects.models import Project
from apps.events.models import Event
from .services import NotificationService

User = get_user_model()


# Examples of events that need notifications
@receiver(post_save, sender=Client)
def handle_new_client(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(is_manager=True)
        for user in users:
            NotificationService.create_notification("new_client", user, {"client": instance}, reference_object=instance)


@receiver(post_save, sender=Project)
def handle_project_status_change(sender, instance, **kwargs):
    if kwargs.get("update_fields") and "status" in kwargs["update_fields"]:
        users = User.objects.filter(is_manager=True)
        for user in users:
            NotificationService.create_notification("project_status_change", user, {"project": instance}, reference_object=instance)
