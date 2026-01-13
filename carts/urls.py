from django.urls import path 
from . import views


urlpatterns = [
    path('add-to-cart/' , views.AddtoCartView.as_view() , name='add-to-cart'),
    path('cart/' , views.CartView.as_view() , name='cart'),
    path('cart/<int:id>/' , views.UpdateDeleteCartItemView.as_view() , name='cart'),
    path("orders/place/", views.PlaceOrderView.as_view(), name="place-order"),
    path("orders/", views.OrderListView.as_view()),
    path("orders/<int:id>/", views.OrderDetailView.as_view()),
    path("orders/<int:id>/status/", views.AdminUpdateOrderStatusView.as_view()),
]