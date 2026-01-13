from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.
class CartItems(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,  related_name="cart_items")
    product=models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "product")
    def __str__(self):
        return f"{self.user.email} - {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES=(
        ("UNPAID", "Unpaid"),
        ("PAID", "Paid"),
        ("CANCELLED", "Cancelled"),
    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name="orders")
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(choices=STATUS_CHOICES , default="UNPAID", max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)
    
class OrderItems(models.Model):
    order=models.ForeignKey(Order , on_delete=models.CASCADE , related_name="items")  
    product=models.ForeignKey(Product , on_delete=models.PROTECT)  
    price=models.DecimalField(max_digits=10 , decimal_places=2)
    quantity=models.PositiveIntegerField()
    

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"