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

    @action(detail=False, methods=['post'])
    def send_slack_message(self, request):
        """
        Endpoint to send a message to Slack immediately
        """
        from .services import send_slack_message
        
        channel = request.data.get('channel')
        message = request.data.get('message')
        
        if not channel or not message:
            return Response(
                {'error': 'Both channel and message are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add # prefix if not already present and not an ID
        if not channel.startswith(('#', 'C', 'D', 'G', 'U')):
            channel = f"#{channel}"
            
        success = send_slack_message(message, channel)
        
        if success:
            return Response(
                {'status': 'Message sent successfully'}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Failed to send message to Slack'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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


@method_decorator(csrf_exempt, name='dispatch')
class SlackTestMessageView(View):
    """
    View for testing Slack message sending
    """
    def get(self, request):
        """
        Display a form for testing Slack message sending
        """
        return HttpResponse("""
            <h1>Test Slack Message</h1>
            <p>Make sure your bot is invited to the channel before sending a message.</p>
            <form method="post" action="">
                <div style="margin-bottom: 15px;">
                    <label for="channel">Channel:</label>
                    <input type="text" id="channel" name="channel" value="general" required style="margin-left: 10px;">
                    <p style="color: #666; margin-top: 5px; font-size: 0.9em;">
                        Use channel name (e.g., "general") or ID. For direct messages, use a user ID.
                    </p>
                </div>
                <div style="margin-bottom: 15px;">
                    <label for="message">Message:</label>
                    <textarea id="message" name="message" required style="display: block; width: 300px; height: 100px; margin-top: 5px;">Hello from Slack Scheduler!</textarea>
                </div>
                <div>
                    <button type="submit" style="background-color: #4A154B; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer;">Send Message</button>
                </div>
            </form>
        """)
    
    def post(self, request):
        """
        Send a test message to Slack
        """
        from .services import send_slack_message
        
        channel = request.POST.get('channel', 'general')
        # Add # prefix if not already present and not an ID
        if not channel.startswith(('#', 'C', 'D', 'G', 'U')):
            channel = f"#{channel}"
            
        message = request.POST.get('message', 'Hello from Slack Scheduler!')
        
        success = send_slack_message(message, channel)
        
        if success:
            return HttpResponse(f"""
                <h1>Success!</h1>
                <p>Message sent to {channel}.</p>
                <p><a href='/api/slack/test-message/'>Send another message</a></p>
            """)
        else:
            return HttpResponse(f"""
                <h1>Error</h1>
                <p>Failed to send message to {channel}.</p>
                <p>Make sure your bot is invited to the channel.</p>
                <p>For public channels, try using the format "#channel_name".</p>
                <p>For private channels and DMs, use the channel/user ID.</p>
                <p><a href='/api/slack/test-message/'>Try again</a></p>
            """)
