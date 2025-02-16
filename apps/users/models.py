from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False, unique=True)
    phone_number = models.CharField(_("phone number"), max_length=20, blank=False)

    class Role(models.TextChoices):
        ADMINISTRATOR = "ADMIN", _("Administrator")
        MANAGER = "MANAGER", _("Manager")

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MANAGER,
    )

    REQUIRED_FIELDS = ["email", "phone_number"]

    def is_administrator(self):
        return self.role == self.Role.ADMINISTRATOR

    def is_manager(self):
        return self.role == self.Role.MANAGER
