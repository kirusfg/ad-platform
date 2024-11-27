from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProjectListView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"


class ProjectDetailView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
