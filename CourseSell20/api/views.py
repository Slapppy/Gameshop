from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count, F
from django.db.models.functions import TruncDate

from api.serializers import UserSerializer
from source.models import Order, User


class OverallOrderStats(APIView):
    def get(self, request):
        total_orders = Order.objects.count()
        total_sum = Order.objects.aggregate(total_sum=Sum('sum_order'))['total_sum']
        avg_sum_per_order = Order.objects.aggregate(avg_sum_per_order=Avg('sum_order'))['avg_sum_per_order']

        stats = {
            'total_orders': total_orders,
            'total_sum': total_sum,
            'avg_sum_per_order': avg_sum_per_order,
        }

        return Response(stats)


class UserStats(APIView):
    def get(self, request):
        most_active_user = User.objects.annotate(order_count=Count('order')).order_by('-order_count').first()
        highest_total_order_user = User.objects.annotate(total_order_sum=Sum('order__sum_order')).order_by(
            '-total_order_sum').first()

        stats = {
            'most_active_user': UserSerializer(most_active_user).data,
            'highest_total_order_user': UserSerializer(highest_total_order_user).data,
        }

        return Response(stats)


class GameStats(APIView):
    def get(self, request):
        most_popular_game = Order.objects.values('game__name').annotate(order_count=Count('game')).order_by(
            '-order_count').first()
        most_profitable_game = Order.objects.values('game__name').annotate(total_order_sum=Sum('sum_order')).order_by(
            '-total_order_sum').first()
        avg_order_sum_per_game = Order.objects.values('game__name').annotate(avg_order_sum=Avg('sum_order')).order_by(
            'game__name')

        stats = {
            'most_popular_game': most_popular_game,
            'most_profitable_game': most_profitable_game,
            'avg_order_sum_per_game': avg_order_sum_per_game,
        }

        return Response(stats)


class DateStats(APIView):
    def get(self, request):
        date_stats = Order.objects.annotate(order_date_truncated=TruncDate('order_date')).values(
            'order_date_truncated').annotate(total_orders=Count('id'), total_sum=Sum('sum_order')).order_by(
            'order_date_truncated')

        stats = {
            'date_stats': date_stats,
        }

        return Response(stats)


class QuantityStats(APIView):
    def get(self, request):
        avg_quantity_per_order = Order.objects.aggregate(avg_quantity_per_order=Avg('quantity'))[
            'avg_quantity_per_order']
        orders_with_specific_quantity = Order.objects.filter(
            quantity=3).count()  # Замените YOUR_SPECIFIC_QUANTITY на конкретное количество товаров

        stats = {
            'avg_quantity_per_order': avg_quantity_per_order,
            'orders_with_specific_quantity': orders_with_specific_quantity,
        }

        return Response(stats)


class PriceStats(APIView):
    def get(self, request):
        avg_price_per_order = Order.objects.annotate(avg_price=F('sum_order') / F('quantity')).aggregate(
            avg_price_per_order=Avg('avg_price'))['avg_price_per_order']

        stats = {
            'avg_price_per_order': avg_price_per_order,
        }

        return Response(stats)


class TimeStats(APIView):
    def get(self, request):
        # Реализуйте статистику по времени заказа, опираясь на поле 'order_date'.
        # Например, вы можете разделить день на утро, день и вечер и посчитать количество заказов в каждом из этих периодов.
        # Для этого можно использовать datetime функции и F() expressions.

        stats = {
            'example_stat': 'Replace with your time-based statistic',
        }

        return Response(stats)
