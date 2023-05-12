
import os
import django
django.setup()
import chats.routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

'''
from fastapi import FastAPI
from starlette.middleware.lifespan import LifespanMiddleware

app = FastAPI()
app.add_middleware(LifespanMiddleware, lifespan="off")
'''

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mapuamates.settings')


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chats.routing.websocket_urlpatterns
        )
    )
})


