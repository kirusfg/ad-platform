from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.clients.models import Client
from apps.channels.models import Channel
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        ON_HOLD = "ON_HOLD", _("On Hold")
        COMPLETED = "COMPLETED", _("Completed")
        CANCELLED = "CANCELLED", _("Cancelled")

    name = models.CharField(_("Name"), max_length=255)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="projects", verbose_name=_("Client"))
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.DRAFT)
    channels = models.ManyToManyField(Channel, through="ProjectChannel", related_name="projects", verbose_name=_("Advertising Channels"))
    deadline = models.DateField(_("Deadline"))
    cost = models.DecimalField(_("Cost"), max_digits=10, decimal_places=2, help_text=_("Total project cost"))
    description = models.TextField(_("Description"), blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_projects", verbose_name=_("Created By"))

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    @property
    def progress(self):
        total_steps = self.steps.count()
        if total_steps == 0:
            return 0
        completed_steps = self.steps.filter(is_completed=True).count()
        return int((completed_steps / total_steps) * 100)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.client}"


class ProjectChannelManager(models.Manager):
    def filter_current(self):
        today = timezone.now().date()
        return self.filter(start_date__lte=today, end_date__gte=today)


class ProjectChannel(models.Model):
    """Intermediate model for Project-Channel relationship with dates and cost"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_channels")
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, related_name="project_channels")
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"))
    cost = models.DecimalField(_("Cost"), max_digits=10, decimal_places=2, help_text=_("Cost for this channel"))
    notes = models.TextField(_("Notes"), blank=True)
    objects = ProjectChannelManager()

    class Meta:
        verbose_name = _("Project Channel")
        verbose_name_plural = _("Project Channels")


class ProjectStep(models.Model):
    """Tasks/Steps in the project including document-related tasks"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="steps")
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    is_completed = models.BooleanField(_("Completed"), default=False)
    due_date = models.DateField(_("Due Date"), null=True, blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Project Step")
        verbose_name_plural = _("Project Steps")
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class ProjectDocument(models.Model):
    class Type(models.TextChoices):
        CONTRACT = "CONTRACT", _("Contract")
        INVOICE = "INVOICE", _("Invoice")
        OTHER = "OTHER", _("Other")

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    type = models.CharField(_("Type"), max_length=20, choices=Type.choices, default=Type.OTHER)
    file = models.FileField(_("File"), upload_to="projects/documents/")
    name = models.CharField(_("Name"), max_length=255)
    uploaded_at = models.DateTimeField(_("Uploaded At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Project Document")
        verbose_name_plural = _("Project Documents")
