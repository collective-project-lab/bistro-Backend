from decimal import Decimal
from uuid import uuid4

from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from cart.views import TAX_RATE

from .models import Order, OrderItem
from .serializers import CheckoutSerializer, OrderSerializer


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects.filter(user=request.user)
            .prefetch_related("items")
            .order_by("-created_at")
        )

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_object_or_404(Cart, user=request.user)

        cart_items = cart.items.select_related("menu_item")

        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subtotal = sum(
            (
                item.menu_item.price * item.quantity
                for item in cart_items
            ),
            Decimal("0.00"),
        )

        tax = (subtotal * TAX_RATE).quantize(Decimal("0.01"))
        total = (subtotal + tax).quantize(Decimal("0.01"))

        shipping = serializer.validated_data["shipping"]

        order = Order.objects.create(
            user=request.user,
            order_number=uuid4().hex[:10].upper(),
            subtotal=subtotal,
            tax=tax,
            total=total,
            shipping_name=shipping["name"],
            shipping_address=shipping["address"],
            shipping_phone=shipping["phone"],
        )

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    menu_item=item.menu_item,
                    name=item.menu_item.name,
                    quantity=item.quantity,
                    price_at_purchase=item.menu_item.price,
                )
                for item in cart_items
            ]
        )

        cart.items.all().delete()

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(
            Order.objects.prefetch_related("items"),
            id=order_id,
            user=request.user,
        )

        serializer = OrderSerializer(order)

        return Response(serializer.data)