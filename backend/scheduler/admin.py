from django.contrib import admin
from .models import ScheduledMessage

# Register your models here.

@admin.register(ScheduledMessage)
class ScheduledMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel', 'scheduled_time', 'status', 'created_at')
    list_filter = ('status', 'channel')
    search_fields = ('message', 'channel')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-scheduled_time',)
