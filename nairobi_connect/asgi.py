import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

# ✅ Set the settings module BEFORE anything else
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nairobi_connect.settings')

# ✅ Create the application only ONCE
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
