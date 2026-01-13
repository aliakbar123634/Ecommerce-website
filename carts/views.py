from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from .serializers import *
from .models import CartItems
from products.models import Product
from products.permission import IsAdmin


class AddtoCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddtoCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        product = get_object_or_404(Product, id=product_id, is_active=True)

        cart_item, created = CartItems.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(
            {
                "message": "Product added to cart",
                "product": product.name,
                "quantity": cart_item.quantity,
            },
            status=status.HTTP_200_OK
        )


class CartView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self , request):
        cart_items=CartItems.objects.filter(user=request.user , product__is_active=True)
        serializer=CartItemSerializer(cart_items , many=True)
        total=sum(
            item.quantity * item.product.price
            for item in cart_items
        )
        return Response(
            {
                "items": serializer.data,
                "total_price": total
            }
        )
    

class UpdateDeleteCartItemView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self , request , id):
        cart_item=get_object_or_404(CartItems , id=id , user=request.user)
        serializer=UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_item.quantity=serializer.validated_data['quantity']
        cart_item.save()
        return Response(
            {
                "message": "cart item updated successfully",
                "quantity":cart_item.quantity,
                "product":cart_item.product.name
            },
            status=status.HTTP_200_OK
        )
    def delete(self , request , id):
        cart_item=get_object_or_404(CartItems , id=id , user=request.user)
        cart_item.delete()
        return Response(
            {
                "message" : "Cart item deleted successsfully"
            },
            status=status.HTTP_200_OK
        )


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart_items = CartItems.objects.filter(
            user=request.user,
            product__is_active=True
        )

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = sum(
            item.product.price * item.quantity
            for item in cart_items
        )

        order = Order.objects.create(
            user=request.user,
            total_price=total
        )

        for item in cart_items:
            OrderItems.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        cart_items.delete()

        return Response(
            {"message": "Order placed successfully", "order_id": order.id},
            status=status.HTTP_201_CREATED
        )
    

class OrderListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        orders=Order.objects.filter(user=request.user).order_by("-id")
        # serializer=OrderItemSerializer(orders, many=True)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
class OrderDetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self , request , id):
        order=get_object_or_404(Order , id=id , user=request.user)
        serializer=OrderSerializer(order)
        return Response(serializer.data , status=status.HTTP_200_OK)  
      
        
        

class AdminUpdateOrderStatusView(APIView):
    permission_classes=[IsAdmin]
    def put(self , request , id):
        order=get_object_or_404(Order , id=id)
        if order.status in ["PAID", "CANCELLED"]:
            return Response(
                {"error": f"Order is already {order.status}. Cannot update."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer=OrderUpdateStatusSerializer(order , data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Order status updated", "order": serializer.data},
            status=status.HTTP_200_OK
        )