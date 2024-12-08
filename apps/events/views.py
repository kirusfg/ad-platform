import json

from django.views.generic import ListView, DetailView
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Event, EventType, EventStatus
from apps.projects.models import Project
from apps.channels.models import Channel
from apps.clients.models import Client


class EventCalendarView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "events/calendar.html"
    context_object_name = "events"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events_json"] = self.get_events_json()
        context["event_types"] = EventType.objects.all()
        context["event_statuses"] = EventStatus.objects.all()
        return context

    def get_events_json(self):
        events_data = []
        for event in self.get_queryset():
            events_data.append(
                {
                    "id": event.id,
                    "title": event.title,
                    "start": event.start_datetime.isoformat(),
                    "end": event.end_datetime.isoformat(),
                    "extendedProps": {
                        "type": event.type.name,
                        "status": event.status.name,
                        "project": event.project.name if event.project else None,
                        "channel": event.channel.name if event.channel else None,
                        "client": event.client.name if event.client else None,
                    },
                    "classNames": [f"event-type-{event.type.name.lower().replace(' ', '-')}", f"event-status-{event.status.name.lower()}"],
                }
            )
        return json.dumps(events_data, cls=DjangoJSONEncoder)


@login_required
def event_create(request):
    if request.method == "GET":
        return TemplateResponse(
            request,
            "events/partials/create_form.html",
            {
                "event_types": EventType.objects.all(),
                "event_statuses": EventStatus.objects.all(),
                "projects": Project.objects.all(),
                "channels": Channel.objects.all(),
                "clients": Client.objects.all(),
            },
        )

    # Handle POST
    event = Event.objects.create(
        title=request.POST["title"],
        description=request.POST["description"],
        type_id=request.POST["type"],
        status_id=request.POST["status"],
        start_datetime=request.POST["start_datetime"],
        end_datetime=request.POST["end_datetime"],
        project_id=request.POST.get("project"),
        channel_id=request.POST.get("channel"),
        client_id=request.POST.get("client"),
    )

    # Return updated events data
    view = EventCalendarView()
    view.object_list = Event.objects.all()  # Set the queryset
    return JsonResponse({"events": json.loads(view.get_events_json())})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "GET":
        return TemplateResponse(
            request,
            "events/partials/edit_form.html",
            {
                "event": event,
                "event_types": EventType.objects.all(),
                "event_statuses": EventStatus.objects.all(),
                "projects": Project.objects.all(),
                "channels": Channel.objects.all(),
                "clients": Client.objects.all(),
            },
        )

    # Handle POST
    event.title = request.POST["title"]
    event.description = request.POST["description"]
    event.type_id = request.POST["type"]
    event.status_id = request.POST["status"]
    event.start_datetime = request.POST["start_datetime"]
    event.end_datetime = request.POST["end_datetime"]
    event.project_id = request.POST.get("project")
    event.channel_id = request.POST.get("channel")
    event.client_id = request.POST.get("client")
    event.save()

    # Return updated events data
    view = EventCalendarView()
    view.object_list = Event.objects.all()
    return JsonResponse({"events": json.loads(view.get_events_json())})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "GET":
        return TemplateResponse(request, "events/partials/delete_confirm.html", {"event": event})

    # Handle POST
    event.delete()

    # Return updated events data
    view = EventCalendarView()
    view.object_list = Event.objects.all()
    return JsonResponse({"events": json.loads(view.get_events_json())})
