from .views import MyTokenRefreshView, RegisterView
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import MyTokenObtainPairView, LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(
        "logout/",
        LogoutView.as_view(next_page=reverse_lazy("game_list")),
        name="logout",
    ),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
