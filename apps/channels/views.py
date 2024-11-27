from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Channel, ChannelType


class ChannelListView(LoginRequiredMixin, ListView):
    model = Channel
    template_name = "channels/list.html"
    context_object_name = "channels"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Channel.Status.choices
        context["channel_types"] = ChannelType.objects.all()
        print(context)
        return context

    def post(self, request, *args, **kwargs):
        try:
            Channel.objects.create(
                name=request.POST.get("name"),
                type_id=request.POST.get("type"),
                location=request.POST.get("location"),
                technical_specs=request.POST.get("technical_specs"),
                comments=request.POST.get("comments"),
                status=Channel.Status.FREE,  # Default status
            )
            messages.success(request, _("Channel created successfully"))
        except Exception as e:
            messages.error(request, _("Error creating channel: %(error)s") % {"error": e})

        return HttpResponseRedirect(reverse_lazy("channels:list"))
