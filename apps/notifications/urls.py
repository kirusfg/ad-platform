from django.urls import path
from .views import mark_as_read, mark_all_as_read

app_name = "notifications"

urlpatterns = [
    path("mark-as-read/<int:pk>/", mark_as_read, name="mark_as_read"),
    path("mark-all-as-read/", mark_all_as_read, name="mark_all_as_read"),
]
