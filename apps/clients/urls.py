from django.urls import path
from . import views

app_name = "clients"

urlpatterns = [
    path("", views.ClientListView.as_view(), name="list"),
    path("create/", views.client_create, name="create"),
    path("<int:pk>/edit/", views.client_edit, name="edit"),
    path("<int:pk>/delete/", views.client_delete, name="delete"),
    path("<int:pk>/", views.ClientDetailView.as_view(), name="detail"),
]
