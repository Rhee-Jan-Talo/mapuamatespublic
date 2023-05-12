from django.urls import path

from accounts import views



urlpatterns = [
    
    path(
        #"register/", views.RegisterAccount.as_view(), name="register-account"
        "register/", views.RegisterAccount, name="register-account"
    ),
    path(
        "login/", views.LoginAccount, name="login"
    ),
    path(
        "verify_account/", views.ConfirmAccount, name="confirm-account"
    ),
    path(
        'create_account/', views.CreateAccount, name="create-account"
    ),
    path(
        'logout_account/', views.LogoutAccount, name="log-out"
    ),
    path(
        'edit_profile/', views.EditProfile, name="edit-profile"
    ),

    
]


