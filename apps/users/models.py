from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMINISTRATOR = "ADMIN", _("Administrator")  # Will be translated to "Администратор"
        MANAGER = "MANAGER", _("Manager")

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MANAGER,
    )

    def is_administrator(self):
        return self.role == self.Role.ADMINISTRATOR

    def is_manager(self):
        return self.role == self.Role.MANAGER
