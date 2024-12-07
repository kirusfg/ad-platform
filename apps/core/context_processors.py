from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def navigation(request):
    nav_items = [
        {
            "name": _("Home"),
            "url": reverse("core:home"),
            "icon": "fa-solid fa-house",
            "active": request.path == reverse("core:home"),
        },
        {
            "name": _("Projects"),
            "url": reverse("projects:list"),
            "icon": "fa-solid fa-user-group",
            "active": request.path.startswith("/projects/"),
        },
        {
            "name": _("Advertising Channels"),
            "url": reverse("channels:list"),
            "icon": "fa-solid fa-tv",
            "active": request.path.startswith("/channels/"),
        },
        {
            "name": _("Clients"),
            "url": reverse("clients:list"),
            "icon": "fa-solid fa-users",
            "active": request.path.startswith("/clients/"),
        },
        {
            "name": _("Events"),
            "url": reverse("events:calendar"),
            "icon": "fa-solid fa-calendar-days",
            "active": request.path.startswith("/events/"),
        },
        {
            "name": _("Analytics"),
            "url": reverse("core:analytics"),
            "icon": "fa-solid fa-chart-bar",
            "active": request.path.startswith("/analytics/"),
        },
    ]
    return {"nav_items": nav_items}
