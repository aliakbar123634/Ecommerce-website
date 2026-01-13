from django.urls import path 
from . import views


urlpatterns = [
    path('products/', views.ProductListView.as_view() , name="products"),
    path('products/<int:pk>' , views.singleProductView.as_view() , name="products" ),
    path('create/' , views.ProductCreateView.as_view(), name="create"),
    path('products/<int:pk>/manage/' , views.ProductDeleteUpdateView.as_view(), name="manage"),
]
