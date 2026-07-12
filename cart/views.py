from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.models import MenuItem

from .models import Cart, CartItem
from .serializers import AddCartItemSerializer, CartItemSerializer, UpdateCartItemSerializer

TAX_RATE = Decimal("0.10")


def get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def build_cart_response(cart):
    items = cart.items.select_related("menu_item")

    subtotal = sum(
        (item.menu_item.price * item.quantity for item in items),
        Decimal("0.00"),
    )

    tax = (subtotal * TAX_RATE).quantize(Decimal("0.01"))
    total = (subtotal + tax).quantize(Decimal("0.01"))

    return {
        "items": CartItemSerializer(items, many=True).data,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
    }


def validate_quantity(value):
    try:
        quantity = int(value)

        if quantity < 1:
            raise ValueError

        return quantity

    except (TypeError, ValueError):
        return None


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_cart(request.user)

        return Response(
            build_cart_response(cart),
            status=status.HTTP_200_OK,
        )


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_cart(request.user)

        menu_item = serializer.validated_data["menu_item"]
        quantity = serializer.validated_data["quantity"]

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults={"quantity": quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(build_cart_response(cart))

class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_cart(request.user)

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart=cart,
        )

        cart_item.quantity = serializer.validated_data["quantity"]
        cart_item.save()

        return Response(build_cart_response(cart))

    def delete(self, request, item_id):
        cart = get_cart(request.user)

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart=cart,
        )

        cart_item.delete()

        return Response(
            build_cart_response(cart),
            status=status.HTTP_200_OK,
        )