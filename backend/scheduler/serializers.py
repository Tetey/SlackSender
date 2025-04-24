from rest_framework import serializers
from .models import ScheduledMessage

class ScheduledMessageSerializer(serializers.ModelSerializer):
    """Serializer for the ScheduledMessage model"""
    class Meta:
        model = ScheduledMessage
        fields = ['id', 'message', 'channel', 'scheduled_time', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']
