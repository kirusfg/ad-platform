from celery import shared_task  # or use cron
from .services import NotificationService


@shared_task
def process_event_reminders():
    NotificationService.process_event_reminders()
