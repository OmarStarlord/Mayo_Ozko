"""
ASGI config for towers project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""



# asgi.py
import os
import pusher
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import consumers  # Update with your actual consumer import

from django.core.asgi import get_asgi_application
from django.conf import settings

# Initialize Pusher with settings
pusher_client = pusher.Pusher(
    app_id=settings.PUSHER['app_id'],
    key=settings.PUSHER['key'],
    secret=settings.PUSHER['secret'],
    cluster=settings.PUSHER['cluster'],
    ssl=settings.PUSHER['ssl']
)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Add your WebSocket routing here
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/some_path/", consumers.YourConsumer.as_asgi()),  # Replace with your consumer
        ])
    ),
})
