from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q

from .models import Project, ProjectChannel, ProjectStep, ProjectDocument
from apps.clients.models import Client
from apps.channels.models import Channel


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/list.html"
    context_object_name = "projects"
    paginate_by = 10
    ordering = ["-created_at"]

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["projects/partials/project_list.html"]
        return [self.template_name]


@login_required
def project_create(request):
    if request.method == "GET":
        return TemplateResponse(
            request,
            "projects/partials/create_form.html",
            {
                "clients": Client.objects.all(),
                "channels": Channel.objects.all(),
                "status_choices": Project.Status.choices,
            },
        )

    # Handle POST
    try:
        with transaction.atomic():
            # Create project
            project = Project.objects.create(
                name=request.POST["name"],
                client_id=request.POST["client"],
                status=request.POST["status"],
                deadline=request.POST["deadline"],
                cost=request.POST["cost"],
                description=request.POST["description"],
            )

            # Create project channels
            channels = request.POST.getlist("channels[]")
            start_dates = request.POST.getlist("channel_start_dates[]")
            end_dates = request.POST.getlist("channel_end_dates[]")
            costs = request.POST.getlist("channel_costs[]")

            for channel, start, end, cost in zip(channels, start_dates, end_dates, costs):
                ProjectChannel.objects.create(project=project, channel_id=channel, start_date=start, end_date=end, cost=cost)

            # Create project steps
            names = request.POST.getlist("step_names[]")
            due_dates = request.POST.getlist("step_due_dates[]")
            orders = request.POST.getlist("step_orders[]")

            for name, due_date, order in zip(names, due_dates, orders):
                ProjectStep.objects.create(project=project, name=name, due_date=due_date or None, order=order)

    except Exception as e:
        return HttpResponse(f"Error creating project: {str(e)}", status=400)

    return TemplateResponse(request, "projects/partials/project_list.html", {"projects": Project.objects.all().order_by("-created_at")})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "GET":
        return TemplateResponse(
            request,
            "projects/partials/edit_form.html",
            {
                "project": project,
                "clients": Client.objects.all(),
                "channels": Channel.objects.all(),
                "status_choices": Project.Status.choices,
            },
        )

    # Handle POST
    try:
        with transaction.atomic():
            # Update project
            project.name = request.POST["name"]
            project.client_id = request.POST["client"]
            project.status = request.POST["status"]
            project.deadline = request.POST["deadline"]
            project.cost = request.POST["cost"]
            project.description = request.POST["description"]
            project.save()

            # Update channels - first remove existing
            project.project_channels.all().delete()

            # Create new channel associations
            channels = request.POST.getlist("channels[]")
            start_dates = request.POST.getlist("channel_start_dates[]")
            end_dates = request.POST.getlist("channel_end_dates[]")
            costs = request.POST.getlist("channel_costs[]")

            for channel, start, end, cost in zip(channels, start_dates, end_dates, costs):
                ProjectChannel.objects.create(project=project, channel_id=channel, start_date=start, end_date=end, cost=cost)

            # Update steps - first remove existing
            project.steps.all().delete()

            # Create new steps
            names = request.POST.getlist("step_names[]")
            due_dates = request.POST.getlist("step_due_dates[]")
            orders = request.POST.getlist("step_orders[]")

            for name, due_date, order in zip(names, due_dates, orders):
                ProjectStep.objects.create(project=project, name=name, due_date=due_date or None, order=order)

    except Exception as e:
        return HttpResponse(f"Error updating project: {str(e)}", status=400)

    return TemplateResponse(request, "projects/partials/project_list.html", {"projects": Project.objects.all().order_by("-created_at")})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "GET":
        return TemplateResponse(request, "projects/partials/delete_confirm.html", {"project": project})

    # Handle POST
    try:
        project.delete()
    except Exception as e:
        return HttpResponse(f"Error deleting project: {str(e)}", status=400)

    return TemplateResponse(request, "projects/partials/project_list.html", {"projects": Project.objects.all().order_by("-created_at")})


@login_required
def toggle_step(request, pk):
    step = get_object_or_404(ProjectStep, pk=pk)
    step.is_completed = not step.is_completed
    step.save()

    return TemplateResponse(
        request, "projects/partials/steps_list.html", {"steps": step.project.steps.all().order_by("order", "created_at")}
    )


@login_required
def upload_document(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "GET":
        return TemplateResponse(
            request, "projects/partials/upload_document.html", {"project": project, "document_types": ProjectDocument.Type.choices}
        )

    # Handle POST
    try:
        doc = ProjectDocument.objects.create(
            project=project, name=request.POST["name"], type=request.POST["type"], file=request.FILES["file"]
        )
    except Exception as e:
        return HttpResponse(str(e), status=400)

    return TemplateResponse(
        request, "projects/partials/documents_list.html", {"documents": project.documents.all().order_by("-uploaded_at")}
    )


@login_required
def delete_document(request, pk):
    doc = get_object_or_404(ProjectDocument, pk=pk)
    project = doc.project

    if request.method == "GET":
        return TemplateResponse(request, "projects/partials/delete_document_confirm.html", {"document": doc})

    # Handle POST
    doc.delete()
    return TemplateResponse(
        request, "projects/partials/documents_list.html", {"documents": project.documents.all().order_by("-uploaded_at")}
    )


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["steps"] = self.object.steps.all().order_by("order", "created_at")
        context["channels"] = self.object.project_channels.select_related("channel")
        context["documents"] = self.object.documents.all().order_by("-uploaded_at")
        return context
