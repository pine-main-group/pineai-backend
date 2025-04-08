from django.urls import path
from .views import JWTLoginView, JWTRegisterView, JWTLogoutView, CheckUserPLan, CheckUserInfo

urlpatterns = [
    path("login/", JWTLoginView.as_view(), name="Login"),
    path("register/", JWTRegisterView.as_view(), name="Register"),
    path("logout/", JWTLogoutView.as_view(), name="Logout"),
    path("checkplan/", CheckUserPLan.as_view(), name="check-plan"),
    path("getuser/", CheckUserInfo.as_view(), name="check-user-info"),
]