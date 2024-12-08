from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.EventCalendarView.as_view(), name="calendar"),
    path("create/", views.event_create, name="create"),
    path("<int:pk>/edit/", views.event_edit, name="edit"),
    path("<int:pk>/delete/", views.event_delete, name="delete"),
]
