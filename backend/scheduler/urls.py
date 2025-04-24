from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'messages', views.ScheduledMessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('slack/auth/', views.SlackAuthView.as_view(), name='slack_auth'),
    path('slack/auth-url/', views.SlackAuthUrlView.as_view(), name='slack_auth_url'),
    path('slack/oauth-callback/', views.SlackOAuthCallbackView.as_view(), name='slack_oauth_callback'),
    path('slack/auth-success/', views.SlackAuthSuccessView.as_view(), name='slack_auth_success'),
    path('slack/auth-error/', views.SlackAuthErrorView.as_view(), name='slack_auth_error'),
    path('slack/test-message/', views.SlackTestMessageView.as_view(), name='slack_test_message'),
]
