from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("", include("apps.users.urls")),
    path("projects/", include("apps.projects.urls")),
    path("channels/", include("apps.channels.urls")),
    path("clients/", include("apps.clients.urls")),
    path("events/", include("apps.events.urls")),
    path("notifications/", include("apps.notifications.urls", namespace="notifications")),
    path("chat/", include("apps.chat.urls", namespace="chat")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
