from django.db import models

class Status(models.TextChoices):
    PLACED = "Placed", "Placed"
    PREPARING = "Preparing", "Preparing"
    DELIVERED = "Delivered", "Delivered"

class Order(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLACED,
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_name = models.CharField(max_length=100)
    shipping_address = models.TextField()
    shipping_phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.user.email}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    menu_item = models.ForeignKey(
        "menu.MenuItem",
        on_delete=models.PROTECT,
    )

    name = models.CharField(max_length=200)

    quantity = models.PositiveIntegerField()

    price_at_purchase = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.name} x {self.quantity} (Order {self.order.order_number})"

'''
Order = {
  id: string
  orderNumber: string
  status: "Placed" | "Preparing" | "Delivered"
  items: { menuItemId: string, name: string, quantity: number, priceAtPurchase: number }[]
  subtotal: number
  tax: number
  total: number
  shippingName: string
  shippingAddress: string
  shippingPhone: string
  createdAt: string  // ISO date string
}'''