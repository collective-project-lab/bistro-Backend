from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from menu.models import MenuItem
from .models import CartItem
from .serializers import CartItemSerializer


class CartApiContractTests(TestCase):
    def test_cart_item_serializer_uses_camelcase_ids(self):
        menu_item = MenuItem(
            id=1,
            name="Burger",
            description="Tasty burger",
            price=Decimal("12.50"),
            category="Main",
            image_url="https://example.com/burger.png",
            is_available=True,
        )
        cart_item = CartItem(id=1, menu_item=menu_item, quantity=2)

        serializer = CartItemSerializer(cart_item)

        self.assertIn("menuItemId", serializer.data)
        self.assertIn("price", serializer.data)
        self.assertNotIn("menu_item", serializer.data)

    def test_cart_item_serializer_returns_string_ids_and_numeric_price(self):
        menu_item = MenuItem(
            id=1,
            name="Burger",
            description="Tasty burger",
            price=Decimal("12.50"),
            category="Main",
            image_url="https://example.com/burger.png",
            is_available=True,
        )
        cart_item = CartItem(id=1, menu_item=menu_item, quantity=2)

        serializer = CartItemSerializer(cart_item)

        self.assertEqual(serializer.data["id"], "1")
        self.assertEqual(serializer.data["menuItemId"], "1")
        self.assertEqual(serializer.data["price"], 12.5)

    def test_cart_route_uses_no_trailing_slash(self):
        self.assertEqual(reverse("cart"), "/api/cart")
        self.assertEqual(reverse("cart-items"), "/api/cart/items")
