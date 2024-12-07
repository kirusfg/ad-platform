from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Channel, ChannelType


class ChannelListView(LoginRequiredMixin, ListView):
    model = Channel
    template_name = "channels/list.html"
    context_object_name = "channels"
    paginate_by = 10
    ordering = ["name"]

    def get(self, request, *args, **kwargs):
        if request.headers.get("HX-Request"):
            self.template_name = "channels/partials/list.html"
        return super().get(request, *args, **kwargs)


class ChannelDetailView(LoginRequiredMixin, DetailView):
    model = Channel
    template_name = "channels/detail.html"
    context_object_name = "channel"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.now().date()

        # Get project channels with related project data
        project_channels = self.object.project_channels.select_related("project", "project__client").order_by("-start_date")
        context["history"] = project_channels

        # Find current usage
        today = timezone.now().date()
        context["current_usage"] = project_channels.filter(start_date__lte=today, end_date__gte=today).first()

        return context


@login_required
def channel_create(request):
    if request.method == "GET":
        return TemplateResponse(request, "channels/partials/create_form.html", {"channel_types": ChannelType.objects.all()})

    # Handle POST
    channel = Channel.objects.create(
        name=request.POST["name"],
        type_id=request.POST["type"],
        location=request.POST["location"],
        technical_specs=request.POST["technical_specs"],
        comments=request.POST["comments"],
    )

    channels = Channel.objects.all()
    return TemplateResponse(request, "channels/partials/list.html", {"channels": channels})


@login_required
def channel_edit(request, pk):
    channel = get_object_or_404(Channel, pk=pk)

    if request.method == "GET":
        return TemplateResponse(
            request, "channels/partials/edit_form.html", {"channel": channel, "channel_types": ChannelType.objects.all()}
        )

    # Handle POST
    channel.name = request.POST["name"]
    channel.type_id = request.POST["type"]
    channel.location = request.POST["location"]
    channel.technical_specs = request.POST["technical_specs"]
    channel.comments = request.POST["comments"]
    channel.save()

    channels = Channel.objects.all()
    return TemplateResponse(request, "channels/partials/list.html", {"channels": channels})


@login_required
def channel_delete(request, pk):
    channel = get_object_or_404(Channel, pk=pk)

    if request.method == "GET":
        return TemplateResponse(request, "channels/partials/delete_confirm.html", {"channel": channel})

    # Handle POST
    channel.delete()

    channels = Channel.objects.all()
    return TemplateResponse(request, "channels/partials/list.html", {"channels": channels})
