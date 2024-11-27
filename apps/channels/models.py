from django.db import models
from django.utils.translation import gettext_lazy as _


class ChannelType(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Channel Type")
        verbose_name_plural = _("Channel Types")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Channel(models.Model):
    class Status(models.TextChoices):
        FREE = "FREE", _("Free")
        RESERVED = "RESERVED", _("Reserved")
        IN_USE = "IN_USE", _("In Use")
        BLOCKED = "BLOCKED", _("Blocked")

    name = models.CharField(_("Name"), max_length=255)
    type = models.ForeignKey(
        ChannelType,
        on_delete=models.PROTECT,  # Prevent deletion of type if channels exist
        verbose_name=_("Type"),
        related_name="channels",
    )
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.FREE)
    location = models.CharField(_("Location"), max_length=255, blank=True)
    technical_specs = models.TextField(_("Technical Specifications"), blank=True)
    comments = models.TextField(_("Comments"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.type.name})"
