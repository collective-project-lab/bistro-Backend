from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    menuItemId = serializers.SerializerMethodField()
    priceAtPurchase = serializers.SerializerMethodField()

    def get_menuItemId(self, obj):
        return str(obj.menu_item_id)

    def get_priceAtPurchase(self, obj):
        return float(obj.price_at_purchase)

    class Meta:
        model = OrderItem
        fields = (
            "menuItemId",
            "name",
            "quantity",
            "priceAtPurchase",
        )

class OrderSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    orderNumber = serializers.CharField(source="order_number", read_only=True)
    shippingName = serializers.CharField(source="shipping_name", read_only=True)
    shippingAddress = serializers.CharField(source="shipping_address", read_only=True)
    shippingPhone = serializers.CharField(source="shipping_phone", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    subtotal = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    def get_id(self, obj):
        return str(obj.id)

    def get_subtotal(self, obj):
        return float(obj.subtotal)

    def get_tax(self, obj):
        return float(obj.tax)

    def get_total(self, obj):
        return float(obj.total)

    class Meta:
        model = Order
        fields = (
            "id",
            "orderNumber",
            "status",
            "items",
            "subtotal",
            "tax",
            "total",
            "shippingName",
            "shippingAddress",
            "shippingPhone",
            "createdAt",
        )


class ShippingSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    address = serializers.CharField()
    phone = serializers.CharField(max_length=15)


class PaymentSerializer(serializers.Serializer):
    cardNumber = serializers.CharField(max_length=19)
    expiry = serializers.CharField(max_length=5)
    cvc = serializers.CharField(max_length=4)
    nameOnCard = serializers.CharField(max_length=100)


class CheckoutSerializer(serializers.Serializer):
    shipping = ShippingSerializer()
    payment = PaymentSerializer()