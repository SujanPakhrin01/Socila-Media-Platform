from App.consumers import NotificationConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r"we/notification/$",NotificationConsumer.as_asgi()),
]
