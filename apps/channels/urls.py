from django.urls import path
from . import views

app_name = "channels"

urlpatterns = [
    path("", views.ChannelListView.as_view(), name="list"),
]
