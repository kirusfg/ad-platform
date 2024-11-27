from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class EventsView(LoginRequiredMixin, TemplateView):
    template_name = "events/calendar.html"
