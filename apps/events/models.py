from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.projects.models import Project
from apps.channels.models import Channel
from apps.clients.models import Client


class EventType(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Event Type")
        verbose_name_plural = _("Event Types")
        ordering = ["name"]

    def __str__(self):
        return self.name


class EventStatus(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Event Status")
        verbose_name_plural = _("Event Statuses")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    type = models.ForeignKey(EventType, on_delete=models.PROTECT, verbose_name=_("Type"), related_name="events")
    status = models.ForeignKey(EventStatus, on_delete=models.PROTECT, verbose_name=_("Status"), related_name="events")

    start_datetime = models.DateTimeField(_("Start Date/Time"))
    end_datetime = models.DateTimeField(_("End Date/Time"))

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_("Project"), related_name="events", null=True, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name=_("Channel"), related_name="events", null=True, blank=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name=_("Client"), related_name="events", null=True, blank=True
    )  # Add this field

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ["start_datetime"]

    def __str__(self):
        return self.title
