from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = "Authenticate"
urlpatterns = [
    path("login/", auth.login, name = "LoginPage"),
    path("logout/", auth.logout, name = "LogoutPage"),
    path("create/account/", auth.createAccount, name = "CreateAccount"),
    path("account/forgot/password/", auth.forgotPassword, name = "ForgotPassword"),
]