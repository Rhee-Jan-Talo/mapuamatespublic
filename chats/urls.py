from django.urls import path

from chats import views


urlpatterns = [
    
    path(
        #"register/", views.RegisterAccount.as_view(), name="register-account"
        "inbox/", views.MessagesInbox, name="messages-inbox"
    ),
    path(
        #"register/", views.RegisterAccount.as_view(), name="register-account"
        "inbox/<thread_id>", views.MessagesInboxSingle, name="messages-inbox-single"
    ),
    path(
        #"register/", views.RegisterAccount.as_view(), name="register-account"
        "start_chat/<user_id>", views.StartChat, name="start-chat"
    ),
]