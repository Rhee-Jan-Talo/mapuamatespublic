from  django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('chats/inbox/', consumers.ChatConsumer.as_asgi()),
    path('chats/inbox/<thread_id>', consumers.ChatConsumer.as_asgi()),
]