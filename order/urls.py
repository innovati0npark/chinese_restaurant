from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('order_detail/<int:pk>/', views.order_detail, name='order_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    
]
