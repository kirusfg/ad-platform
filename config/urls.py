from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("projects/", include("apps.projects.urls")),
    path("channels/", include("apps.channels.urls")),
    path("clients/", include("apps.clients.urls")),
    path("events/", include("apps.events.urls")),
]
