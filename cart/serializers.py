from rest_framework import serializers

from menu.models import MenuItem
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    menuItemId = serializers.SerializerMethodField(source="menu_item.id")

    name = serializers.CharField(
        source="menu_item.name",
        read_only=True,
    )

    price = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.id)

    def get_menuItemId(self, obj):
        return str(obj.menu_item_id)

    def get_price(self, obj):
        return float(obj.menu_item.price)

    class Meta:
        model = CartItem
        fields = (
            "id",
            "menuItemId",
            "name",
            "price",
            "quantity",
        )


class AddCartItemSerializer(serializers.Serializer):
    menuItemId = serializers.PrimaryKeyRelatedField(
        source="menu_item",
        queryset=MenuItem.objects.filter(is_available=True),
    )

    quantity = serializers.IntegerField(min_value=1)


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)