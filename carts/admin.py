from django.contrib import admin

# Register your models here.
from .models import *
# class CartItemsAdmin(admin.ModelAdmin):
#     list_display = ['user', 'product', 'quantity', 'created_at']
admin.site.register(CartItems)