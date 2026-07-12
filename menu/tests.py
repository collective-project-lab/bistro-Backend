from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import MenuItem
from .serializers import MenuItemSerializer


class MenuApiContractTests(TestCase):
    def test_menu_serializer_exposes_camelcase_image_url_field(self):
        menu_item = MenuItem(
            id=1,
            name="Burger",
            description="Tasty burger",
            price=Decimal("12.50"),
            category="Main",
            image_url="https://example.com/burger.png",
            is_available=True,
        )

        serializer = MenuItemSerializer(menu_item)

        self.assertIn("imageUrl", serializer.data)
        self.assertEqual(serializer.data["imageUrl"], "https://example.com/burger.png")

    def test_menu_route_uses_no_trailing_slash(self):
        self.assertEqual(reverse("menu-item-list"), "/api/menu")
