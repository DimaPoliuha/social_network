from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    # ex: /
    path("", views.IndexView.as_view(), name="index"),
    # ex: /5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /5/like/
    path("<int:post_id>/like/", views.like, name="like"),
]
