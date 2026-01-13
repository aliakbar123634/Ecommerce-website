from rest_framework import serializers
from . models import *

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model=Product
        fields=(            
            "id",
            "name",
            "description",
            "price",
            "stock",
            "image",
            )