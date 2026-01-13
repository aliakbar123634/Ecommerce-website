from rest_framework import serializers
from .models import *
class AddtoCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = (
            "id",
            "product_name",
            "product_price",
            "quantity",
            "subtotal",
        )

    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity
    
class UpdateCartItemSerializer(serializers.Serializer):
    quantity=serializers.IntegerField(min_value=1)    


class OrderItemSerializer(serializers.ModelSerializer):
    # product_name = serializers.CharField(source="product.name", read_only=True)
    subtotal=serializers.SerializerMethodField()
    class Meta:
        model=OrderItems
        fields=(
            "product",
            "price",
            "quantity",
            "subtotal",
        ) 

    def get_subtotal(self , obj):
        return obj.price * obj.quantity

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True , read_only=True)
    class Meta:
        model=Order
        fields=(
            "id",
            "total_price",
            "status",
            "created_at",
            "items",
        )   


class OrderUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=("status",)

    def validate_status(self, value):
        if value not in dict(Order.STATUS_CHOICES).keys(): 
            raise serializers.ValidationError("Invalid status value.")  
        return value