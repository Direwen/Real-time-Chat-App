"""
ASGI config for chatsystem project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from chat.routing import websocket_urlpatterns
from chat.middlewares import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatsystem.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    
    "websocket": JWTAuthMiddleware(
            #AuthMiddlewareStack will populate the connection’s scope with a reference to the currently authenticated user
            AuthMiddlewareStack(
                URLRouter(websocket_urlpatterns)
            )
        ),
})
