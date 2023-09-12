from django.urls import path
from .views import (
    OverallOrderStats,
    UserStats,
    GameStats,
    DateStats,
    QuantityStats,
    PriceStats,
    OrderListWeek,
    DailyRevenueView,
    MonthlyRevenueView

)

urlpatterns = [
    path(
        "overall_order_stats/", OverallOrderStats.as_view(), name="overall-order-stats"
    ),
    path("user_stats/", UserStats.as_view(), name="user-stats"),
    path("game_stats/", GameStats.as_view(), name="game-stats"),
    path("date_stats/", DateStats.as_view(), name="date-stats"),
    path("quantity_stats/", QuantityStats.as_view(), name="quantity-stats"),
    path("price_stats/", PriceStats.as_view(), name="price-stats"),
    path('orders/week/', OrderListWeek.as_view(), name='order-list-week'),
    path('daily-revenue/', DailyRevenueView.as_view(), name='daily-revenue'),
    path('monthly-revenue/', MonthlyRevenueView.as_view(), name='monthly-revenue'),

]
