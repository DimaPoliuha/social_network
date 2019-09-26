from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from . import views

app_name = "api"

router = routers.DefaultRouter()
router.register(r"posts", views.PostViewSet)
router.register(r"users", views.UserViewSet)
router.register(r"likes", views.LikeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
