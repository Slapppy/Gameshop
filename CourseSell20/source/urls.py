from django.urls import path
from source import views
from django.conf import settings
from django.conf.urls.static import static
from source.views import GameListView, ProfileView, AddGameView

urlpatterns = [
    path("", GameListView.as_view(), name="game_list"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("addgame/", AddGameView.as_view(), name="addgame"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
