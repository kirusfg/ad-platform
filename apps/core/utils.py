from django.conf import settings
from django.utils import timezone


def get_current_timezone():
    """Utility function to get current timezone"""
    return timezone.get_current_timezone()
