from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone

from .models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/list.html"
    context_object_name = "clients"
    paginate_by = 10
    ordering = ["name"]  # Order clients alphabetically

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["clients/partials/list.html"]
        return [self.template_name]


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "clients/detail.html"
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get active projects (not completed or cancelled)
        context["active_projects"] = self.object.projects.filter(~Q(status__in=["COMPLETED", "CANCELLED"])).order_by("deadline")

        # Get completed/cancelled projects
        context["completed_projects"] = self.object.projects.filter(status__in=["COMPLETED", "CANCELLED"]).order_by("-created_at")

        # Calculate statistics
        stats = {
            "total_projects": self.object.projects.count(),
            "active_projects": context["active_projects"].count(),
            "total_spent": self.object.projects.aggregate(total=Sum("cost"))["total"] or 0,
            "avg_project_cost": self.object.projects.aggregate(avg=Avg("cost"))["avg"] or 0,
        }
        context["stats"] = stats

        return context


@login_required
def client_create(request):
    if request.method == "GET":
        return TemplateResponse(request, "clients/partials/create_form.html", {})

    # Handle POST
    client = Client.objects.create(
        name=request.POST["name"],
        contact_person=request.POST["contact_person"],
        email=request.POST["email"],
        phone=request.POST["phone"],
        address=request.POST["address"],
        notes=request.POST["notes"],
    )

    clients = Client.objects.all()
    return TemplateResponse(request, "clients/partials/list.html", {"clients": clients})


@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "GET":
        return TemplateResponse(request, "clients/partials/edit_form.html", {"client": client})

    # Handle POST
    client.name = request.POST["name"]
    client.contact_person = request.POST["contact_person"]
    client.email = request.POST["email"]
    client.phone = request.POST["phone"]
    client.address = request.POST["address"]
    client.notes = request.POST["notes"]
    client.save()

    clients = Client.objects.all()
    return TemplateResponse(request, "clients/partials/list.html", {"clients": clients})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "GET":
        return TemplateResponse(request, "clients/partials/delete_confirm.html", {"client": client})

    # Handle POST
    client.delete()

    clients = Client.objects.all()
    return TemplateResponse(request, "clients/partials/list.html", {"clients": clients})
