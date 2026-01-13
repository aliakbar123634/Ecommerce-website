from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permission import *
from rest_framework.parsers import MultiPartParser , FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from .filters import *

# Create your views here.
# class ProductListView(APIView):
#     def get(self, request):
#         products=Product.objects.filter(is_active=True)
#         serializer=ProductSerializer(products , many=True)
#         return Response(serializer.data , status=status.HTTP_200_OK)

class ProductListView(generics.ListAPIView):
    queryset=Product.objects.filter(is_active=True)
    serializer_class=ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
class singleProductView(APIView):
    def get(self, request , pk):
        product=get_object_or_404(Product , pk=pk ,is_active=True)
        serializer=ProductSerializer(product)
        return Response(serializer.data , status=status.HTTP_200_OK)


class ProductCreateView(APIView):
    permission_classes=[IsAdmin]
    parser_classes=[MultiPartParser , FormParser]

    def post(self , request):
        serializer=ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_201_CREATED)
    
class ProductDeleteUpdateView(APIView):
    permission_classes=[IsAdmin]
    def put(self , request , pk):
        product=get_object_or_404(Product , pk=pk)
        serializer=ProductSerializer(product , data=request.data , partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self , request , pk):
        product=get_object_or_404(Product ,is_active=True, pk=pk)
        product.is_active=False
        product.save()
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
