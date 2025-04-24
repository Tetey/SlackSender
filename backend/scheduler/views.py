from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ScheduledMessage
from .serializers import ScheduledMessageSerializer

# Create your views here.

class ScheduledMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for scheduled Slack messages
    """
    queryset = ScheduledMessage.objects.all().order_by('-scheduled_time')
    serializer_class = ScheduledMessageSerializer
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """
        Endpoint to simulate sending a message to Slack
        In a real application, this would integrate with the Slack API
        """
        message_id = request.data.get('id')
        try:
            message = ScheduledMessage.objects.get(id=message_id)
            # In a real application, we would send the message to Slack here
            # For now, we'll just update the status
            message.status = 'sent'
            message.save()
            return Response({'status': 'Message sent successfully'}, status=status.HTTP_200_OK)
        except ScheduledMessage.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
