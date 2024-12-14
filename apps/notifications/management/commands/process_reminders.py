from django.core.management.base import BaseCommand
from apps.notifications.services import NotificationService


class Command(BaseCommand):
    help = "Process event reminders"

    def handle(self, *args, **options):
        NotificationService.process_event_reminders()
