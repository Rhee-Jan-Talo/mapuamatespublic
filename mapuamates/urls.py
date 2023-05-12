
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', views.Home, name="home"),
    path("chats/", include("chats.urls")),
    path("accounts/", include("accounts.urls")),
    path("discussions/", include("discussions.urls")),
]
