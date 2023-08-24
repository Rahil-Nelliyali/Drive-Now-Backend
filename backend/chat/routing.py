from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from . import consumers

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(
            [
                path("ws/chat/<int:room_name>/", consumers.ChatConsumer.as_asgi()),
            ]
        ),
    }
)
