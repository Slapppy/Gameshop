from rest_framework import generics
from django.db.models import Sum, Avg, Count, F
from django.db.models.functions import TruncDate
from .serializers import OrderSerializer
from api.serializers import UserSerializer
from source.models import Order, User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta


class OverallOrderStats(APIView):
    def get(self, request):
        total_orders = Order.objects.count()
        total_sum = Order.objects.aggregate(total_sum=Sum("sum_order"))["total_sum"]
        avg_sum_per_order = Order.objects.aggregate(avg_sum_per_order=Avg("sum_order"))[
            "avg_sum_per_order"
        ]

        stats = {
            "total_orders": total_orders,
            "total_sum": total_sum,
            "avg_sum_per_order": avg_sum_per_order,
        }

        return Response(stats)


class UserStats(APIView):
    def get(self, request):
        most_active_user = (
            User.objects.annotate(order_count=Count("order"))
            .order_by("-order_count")
            .first()
        )
        highest_total_order_user = (
            User.objects.annotate(total_order_sum=Sum("order__sum_order"))
            .order_by("-total_order_sum")
            .first()
        )

        stats = {
            "most_active_user": UserSerializer(most_active_user).data,
            "highest_total_order_user": UserSerializer(highest_total_order_user).data,
        }

        return Response(stats)


class GameStats(APIView):
    def get(self, request):
        most_popular_game = (
            Order.objects.values("game__name")
            .annotate(order_count=Count("game"))
            .order_by("-order_count")
            .first()
        )
        most_profitable_game = (
            Order.objects.values("game__name")
            .annotate(total_order_sum=Sum("sum_order"))
            .order_by("-total_order_sum")
            .first()
        )
        avg_order_sum_per_game = (
            Order.objects.values("game__name")
            .annotate(avg_order_sum=Avg("sum_order"))
            .order_by("game__name")
        )

        stats = {
            "most_popular_game": most_popular_game,
            "most_profitable_game": most_profitable_game,
            "avg_order_sum_per_game": avg_order_sum_per_game,
        }

        return Response(stats)


class DateStats(APIView):
    def get(self, request):
        date_stats = (
            Order.objects.annotate(order_date_truncated=TruncDate("order_date"))
            .values("order_date_truncated")
            .annotate(total_orders=Count("id"), total_sum=Sum("sum_order"))
            .order_by("order_date_truncated")
        )

        stats = {
            "date_stats": date_stats,
        }

        return Response(stats)


class QuantityStats(APIView):
    def get(self, request):
        avg_quantity_per_order = Order.objects.aggregate(
            avg_quantity_per_order=Avg("quantity")
        )["avg_quantity_per_order"]
        orders_with_specific_quantity = Order.objects.filter(
            quantity=3
        ).count()

        stats = {
            "avg_quantity_per_order": avg_quantity_per_order,
            "orders_with_specific_quantity": orders_with_specific_quantity,
        }

        return Response(stats)


class PriceStats(APIView):
    def get(self, request):
        avg_price_per_order = Order.objects.annotate(
            avg_price=F("sum_order") / F("quantity")
        ).aggregate(avg_price_per_order=Avg("avg_price"))["avg_price_per_order"]

        stats = {
            "avg_price_per_order": avg_price_per_order,
        }

        return Response(stats)


# class TimeStats(APIView):
#     def get(self, request):
#
#         stats = {
#             "example_stat": "stat",
#         }
#
#         return Response(stats)


class OrderListWeek(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        one_week_ago = timezone.now() - timedelta(days=7)
        queryset = Order.objects.filter(order_date__gte=one_week_ago)
        return queryset


class DailyRevenueView(APIView):
    def get(self, request, format=None):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        daily_revenue = Order.objects.filter(order_date__date=today).aggregate(Sum('sum_order'))['sum_order__sum'] or 0

        yesterday_revenue = Order.objects.filter(order_date__date=yesterday).aggregate(Sum('sum_order'))[
                                'sum_order__sum'] or 0

        revenue_change = daily_revenue - yesterday_revenue
        revenue_change_percentage = (revenue_change / yesterday_revenue) * 100 if yesterday_revenue > 0 else 0

        response_data = {
            "daily_revenue": daily_revenue,
            "revenue_change": revenue_change,
            "revenue_change_percentage": revenue_change_percentage
        }

        return Response(response_data, status=status.HTTP_200_OK)


class MonthlyRevenueView(APIView):
    def get(self, request, format=None):
        # Вычислите начальную и конечную даты для месячной выручки
        today = timezone.now().date()
        last_month_start = today - timedelta(days=today.day)
        last_month_end = today - timedelta(days=1)

        # Получите сумму заказов за прошлый месяц
        monthly_revenue = Order.objects.filter(order_date__date__gte=last_month_start,
                                               order_date__date__lte=last_month_end).aggregate(Sum('sum_order'))[
                              'sum_order__sum'] or 0

        # Вычислите изменение выручки
        last_month_start_prev_year = last_month_start - timedelta(days=365)
        last_month_end_prev_year = last_month_end - timedelta(days=365)
        last_year_revenue = Order.objects.filter(order_date__date__gte=last_month_start_prev_year,
                                                 order_date__date__lte=last_month_end_prev_year).aggregate(
            Sum('sum_order'))['sum_order__sum'] or 0
        revenue_change = monthly_revenue - last_year_revenue
        revenue_change_percentage = (revenue_change / last_year_revenue) * 100 if last_year_revenue > 0 else 0

        # Верните данные в формате JSON
        response_data = {
            "monthly_revenue": monthly_revenue,
            "revenue_change": revenue_change,
            "revenue_change_percentage": revenue_change_percentage
        }

        return Response(response_data, status=status.HTTP_200_OK)
