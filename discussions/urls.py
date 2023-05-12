from django.urls import path

from discussions import views



urlpatterns = [
    
    path(
        #"register/", views.RegisterAccount.as_view(), name="register-account"
        "boards/", views.DiscussionBoard, name="discussion-board"
    ),

    path(
        #"register/", views.RegisterAccount.as_view(), name="register-account"
        "boards/details/<discussion_id>", views.DiscussionDetails, name="discussion-details"
    ),

    path(
        #"register/", views.RegisterAccount.as_view(), name="register-account"
        "boards/create_board", views.CreateBoard, name="create-board"
    ),

    path(
        #"register/", views.RegisterAccount.as_view(), name="register-account"
        "boards/comment/<discussion_id>", views.SendComment, name="send-comment"
    ),

    path(
        #"register/", views.RegisterAccount.as_view(), name="register-account"
        "boards/delete_comment/<discussion_id>/<discussion_comment_id>", views.DeleteComment, name="delete-comment"
    ),


    path(
        #"register/", views.RegisterAccount.as_view(), name="register-account"
        "boards/delete_post/<discussion_id>", views.DeletePost, name="delete-post"
    ),

    path(
        #"register/", views.RegisterAccount.as_view(), name="register-account"
        "boards/edit_post/<discussion_id>", views.EditPost, name="edit-post"
    ),

    
]


