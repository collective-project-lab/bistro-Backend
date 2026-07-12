from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Order
from .serializers import OrderSerializer


class OrderApiContractTests(TestCase):
    def test_order_serializer_uses_camelcase_field_names(self):
        order = Order(
            id=1,
            order_number="A123",
            status="Placed",
            subtotal=Decimal("12.50"),
            tax=Decimal("1.25"),
            total=Decimal("13.75"),
            shipping_name="Alice",
            shipping_address="123 Main St",
            shipping_phone="555-1234",
        )

        serializer = OrderSerializer(order)

        self.assertIn("orderNumber", serializer.fields)
        self.assertIn("shippingName", serializer.fields)
        self.assertIn("shippingAddress", serializer.fields)
        self.assertIn("shippingPhone", serializer.fields)
        self.assertIn("createdAt", serializer.fields)

    def test_order_serializer_returns_string_ids_and_numeric_amounts(self):
        order = Order(
            id=1,
            order_number="A123",
            status="Placed",
            subtotal=Decimal("12.50"),
            tax=Decimal("1.25"),
            total=Decimal("13.75"),
            shipping_name="Alice",
            shipping_address="123 Main St",
            shipping_phone="555-1234",
        )

        serializer = OrderSerializer(order)
        data = serializer.data

        self.assertEqual(data["id"], "1")
        self.assertEqual(data["orderNumber"], "A123")
        self.assertEqual(data["subtotal"], 12.5)
        self.assertEqual(data["tax"], 1.25)
        self.assertEqual(data["total"], 13.75)

    def test_order_route_uses_no_trailing_slash(self):
        self.assertEqual(reverse("order-list"), "/api/orders")
        self.assertEqual(reverse("order-detail", kwargs={"order_id": 1}), "/api/orders/1")
