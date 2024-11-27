from django.utils.translation import gettext_lazy as _


def navigation(request):
    nav_items = [
        {
            "name": _("Home"),
            "url": "/",
            "active": request.path == "/",
        },
        {
            "name": _("Projects"),
            "url": "/projects/",
            "active": request.path.startswith("/projects/"),
        },
        {
            "name": _("Advertising Channels"),
            "url": "/channels/",
            "active": request.path.startswith("/channels/"),
        },
        {
            "name": _("Clients"),
            "url": "/clients/",
            "active": request.path.startswith("/clients/"),
        },
        {
            "name": _("Events"),
            "url": "/events/",
            "active": request.path.startswith("/events/"),
        },
    ]
    return {"nav_items": nav_items}
