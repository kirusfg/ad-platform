from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta, datetime
import pytz

from apps.projects.models import Project
from apps.clients.models import Client
from apps.channels.models import Channel


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Set fixed date to May 18, 2025
        today = datetime(2024, 12, 8, tzinfo=pytz.UTC).date()
        thirty_days_ago = today - timedelta(days=30)

        # Overview statistics
        context["stats"] = {
            "total_active_projects": Project.objects.exclude(status__in=["COMPLETED", "CANCELLED"]).count(),
            "total_revenue": Project.objects.filter(status="COMPLETED").aggregate(total=Sum("cost"))["total"] or 0,
            "projects_this_month": Project.objects.filter(created_at__gte=thirty_days_ago).count(),
            "active_clients": Client.objects.filter(projects__status="IN_PROGRESS").distinct().count(),
        }

        # Projects by status
        status_data = Project.objects.values("status").annotate(count=Count("id")).order_by("status")
        context["project_status_data"] = {
            "labels": [status["status"] for status in status_data],
            "data": [status["count"] for status in status_data],
        }

        # Revenue over time (last 12 months)
        twelve_months_ago = today - timedelta(days=365)

        # Generate all months in the range
        months = []
        current = twelve_months_ago
        while current <= today:
            months.append(current.replace(day=1))
            # Move to first day of next month
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)

        # Get revenue data based on project end dates (deadline)
        revenue_data = (
            Project.objects.filter(status="COMPLETED")
            .filter(deadline__gte=twelve_months_ago, deadline__lte=today)
            .annotate(month=TruncMonth("deadline"))
            .values("month")
            .annotate(total=Sum("cost"))
            .order_by("month")
        )

        # Convert to dictionary for easy lookup
        revenue_by_month = {entry["month"]: float(entry["total"]) for entry in revenue_data}  # Removed .date()

        # Create final data with all months
        complete_revenue_data = [{"month": month, "total": revenue_by_month.get(month, 0.0)} for month in months]

        context["revenue_data"] = {
            "labels": [entry["month"].strftime("%B %Y") for entry in complete_revenue_data],
            "data": [entry["total"] for entry in complete_revenue_data],
        }

        # Channel usage
        channel_data = (
            Channel.objects.annotate(usage_count=Count("project_channels")).values("name", "usage_count").order_by("-usage_count")[:5]
        )
        context["channel_data"] = {
            "labels": [channel["name"] for channel in channel_data],
            "data": [channel["usage_count"] for channel in channel_data],
        }

        # Client activity
        client_data = (
            Client.objects.annotate(project_count=Count("projects"), total_spent=Sum("projects__cost"))
            .values("name", "project_count", "total_spent")
            .order_by("-project_count")[:5]
        )
        context["client_data"] = {
            "labels": [client["name"] for client in client_data],
            "projects": [client["project_count"] for client in client_data],
            "spent": [float(client["total_spent"] or 0) for client in client_data],
        }

        # Recent activity
        context["recent_projects"] = Project.objects.order_by("-created_at")[:5]
        context["upcoming_deadlines"] = Project.objects.filter(status="IN_PROGRESS").filter(deadline__gte=today).order_by("deadline")[:5]

        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
