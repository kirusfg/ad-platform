from django.contrib import admin
from .models import Event, EventType, EventStatus


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(EventStatus)
class EventStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "status", "start_datetime", "end_datetime", "project", "channel")
    list_filter = ("type", "status", "project", "channel")
    search_fields = ("title", "description")
    ordering = ("-start_datetime",)
