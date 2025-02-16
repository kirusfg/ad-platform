from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "phone_number", "role", "is_active")
    list_filter = ("role", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone_number")}),
        (
            _("Permissions"),
            {"fields": ("role", "is_active")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "phone_number", "password1", "password2", "role"),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        # Only allow non-superusers limited access; for superusers include all fields.
        if not request.user.is_superuser:
            self.exclude = (
                "role",
                "is_active",
                "email",
                "phone_number",
            )
        else:
            self.exclude = None
        return super().get_form(request, obj, **kwargs)
