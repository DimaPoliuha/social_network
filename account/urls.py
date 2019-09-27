from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "account"
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("activate/<slug:uidb64>/<slug:token>/", views.activate, name="activate"),
    path(
        "signin/",
        auth_views.LoginView.as_view(
            template_name="account/signin.html", redirect_authenticated_user=True
        ),
        name="signin",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
