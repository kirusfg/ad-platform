from django.contrib import admin
from .models import Channel, ChannelType


@admin.register(ChannelType)
class ChannelTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "status", "location", "created_at")
    list_filter = ("type", "status")
    search_fields = ("name", "location", "technical_specs", "comments")
    ordering = ("-created_at",)
