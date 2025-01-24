from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.models import Orders, Dishes
from api.serializers import OrderSerializer, DishSerializer
from django.db.models import Sum
from rest_framework.request import Request
from typing import Dict, Any


class DishViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления блюдами.
    """

    queryset = Dishes.objects.all()
    serializer_class = DishSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления заказами.
    """

    queryset = Orders.objects.all()
    serializer_class = OrderSerializer


class ReportViewSet(APIView):
    """
    APIView для получения отчета о выручке за день.
    """

    def get(self, request: Request) -> Response:
        """
        Возвращает выручку за текущий день.
        """
        try:
            today = datetime.now()
            start_of_shift = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_shift = today.replace(
                hour=23, minute=59, second=59, microsecond=999999
            )
            report = (
                Orders.objects.filter(
                    status=Orders.Status.ГОТОВ,
                    created_at__range=(start_of_shift, end_of_shift),
                ).aggregate(total_revenue=Sum("total_price"))["total_revenue"]
                or 0
            )
            if report:
                return Response(
                    {"message": f"Выручка за день составила {report} руб."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Выручки за сегодня нет"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": f"Ошибка {e}"}, status=status.HTTP_400_BAD_REQUEST
            )
