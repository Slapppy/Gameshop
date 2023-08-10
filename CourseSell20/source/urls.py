from django.urls import path
from source import views
from django.conf import settings
from django.conf.urls.static import static
from source.views import GameListView, ProfileView, AddGameView, BalanceView, CartListView

urlpatterns = [
    path("", GameListView.as_view(), name="game_list"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("addgame/", AddGameView.as_view(), name="addgame"),
    path('balance/', BalanceView.as_view(), name='balance'),
    path('cart/', CartListView.as_view(), name='cart'),

]
