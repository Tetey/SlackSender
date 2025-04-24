from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ScheduledMessageViewSet, 
    SlackAuthView, 
    SlackOAuthCallbackView,
    SlackAuthSuccessView,
    SlackAuthErrorView,
    SlackTestMessageView
)

router = DefaultRouter()
router.register(r'messages', ScheduledMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('slack/auth/', SlackAuthView.as_view(), name='slack_auth'),
    path('slack/oauth-callback/', SlackOAuthCallbackView.as_view(), name='slack_oauth_callback'),
    path('slack/auth-success/', SlackAuthSuccessView.as_view(), name='slack_auth_success'),
    path('slack/auth-error/', SlackAuthErrorView.as_view(), name='slack_auth_error'),
    path('slack/test-message/', SlackTestMessageView.as_view(), name='slack_test_message'),
]
