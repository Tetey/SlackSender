from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from .models import ScheduledMessage
from .serializers import ScheduledMessageSerializer
from .slack_auth import get_authorize_url, handle_oauth_callback

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


class SlackAuthView(View):
    """
    View for initiating Slack OAuth flow
    """
    def get(self, request):
        """
        Redirect the user to the Slack authorization page
        """
        authorize_url, _ = get_authorize_url(request)
        return redirect(authorize_url)


@method_decorator(csrf_exempt, name='dispatch')
class SlackOAuthCallbackView(View):
    """
    View for handling Slack OAuth callback
    """
    def get(self, request):
        """
        Handle the OAuth callback from Slack
        """
        return handle_oauth_callback(request)


class SlackAuthSuccessView(View):
    """
    View for displaying a success message after Slack authentication
    """
    def get(self, request):
        """
        Display a success message
        """
        return HttpResponse("<h1>Slack Authentication Successful!</h1><p>You can now close this window and return to the app.</p>")


class SlackAuthErrorView(View):
    """
    View for displaying an error message after Slack authentication
    """
    def get(self, request):
        """
        Display an error message
        """
        return HttpResponse("<h1>Slack Authentication Failed</h1><p>There was an error authenticating with Slack. Please try again.</p>")
