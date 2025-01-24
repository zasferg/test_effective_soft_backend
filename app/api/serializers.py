from rest_framework import serializers
from orders.models import Orders, Dishes
from typing import Dict, Any


class DishSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Dishes.
    """

    class Meta:
        model = Dishes
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Orders.
    """

    items = DishSerializer(many=True, read_only=True)
    items_ids = serializers.PrimaryKeyRelatedField(
        queryset=Dishes.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Orders
        fields = [
            "id",
            "table_number",
            "status",
            "items",
            "items_ids",
            "total_price",
            "created_at",
        ]
        read_only_fields = ["total_price", "created_at"]

    def create(self, validated_data: Dict[str, Any]) -> Orders:
        """
        Создает новый заказ с указанными блюдами.
        """

        items = validated_data.pop("items_ids")
        order = Orders(
            table_number=validated_data["table_number"], status=validated_data["status"]
        )
        order.save()
        order.items.add(*items)
        order.save()
        return order

    def update(self, instance: Orders, validated_data: Dict[str, Any]) -> Orders:
        """
        Обновляет существующий заказ с указанными блюдами.
        """
        items = validated_data.pop("items_ids")
        instance.table_number = validated_data.get(
            "table_number", instance.table_number
        )
        instance.status = validated_data.get("status", instance.status)
        instance.items.set(items)
        instance.save()
        return instance
