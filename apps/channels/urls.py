from django.urls import path
from . import views

app_name = "channels"

urlpatterns = [
    path("", views.ChannelListView.as_view(), name="list"),
    path("create/", views.channel_create, name="create"),
    path("<int:pk>/edit/", views.channel_edit, name="edit"),
    path("<int:pk>/delete/", views.channel_delete, name="delete"),
    path("<int:pk>/", views.ChannelDetailView.as_view(), name="detail"),
]
