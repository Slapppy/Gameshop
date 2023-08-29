from django.urls import path
from django.views.generic import TemplateView

from source.views import (
    GameListView,
    ProfileView,
    AddGameView,
    BalanceView,
    CartListView,
    ProductDetailView,
    AddToCartView,
    RemoveFromCartView,
    RemoveCartItemView,
    CheckoutView,
    SuccessPay,
    NoBalance,
    SubmitReviewView,
    DashBoard,
)

urlpatterns = [
    path("", GameListView.as_view(), name="game_list"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("addgame/", AddGameView.as_view(), name="addgame"),
    path("balance/", BalanceView.as_view(), name="balance"),
    path("game/<int:id>", ProductDetailView.as_view(), name="game_detail"),
    path("cart/", CartListView.as_view(), name="cart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("add-to-cart/<int:game_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path(
        "remove-from-cart/<int:cart_id>/",
        RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
    path(
        "remove-cart-item/<int:pk>/",
        RemoveCartItemView.as_view(),
        name="remove_cart_item",
    ),
    path("success/", SuccessPay.as_view(), name="SuccessPay"),
    path("nobalance/", NoBalance.as_view(), name="NoBalance"),
    path("dashboard/", DashBoard.as_view(), name="dashboard"),
    path(
        "submitreview/<int:game_id>/", SubmitReviewView.as_view(), name="submitreview"
    ),
    path(
        "grafana-graph/",
        TemplateView.as_view(template_name="source/graph.html"),
        name="grafana-graph",
    ),
]
