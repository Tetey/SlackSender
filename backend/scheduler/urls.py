from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduledMessageViewSet

router = DefaultRouter()
router.register(r'messages', ScheduledMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
