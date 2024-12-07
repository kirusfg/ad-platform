from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="list"),
    path("create/", views.project_create, name="create"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="detail"),
    path("<int:pk>/edit", views.project_edit, name="edit"),
    path("<int:pk>/delete", views.project_delete, name="delete"),
    path("steps/<int:pk>/toggle/", views.toggle_step, name="toggle_step"),
    path("<int:pk>/upload-document/", views.upload_document, name="upload_document"),
    path("documents/<int:pk>/delete/", views.delete_document, name="delete_document"),
]
