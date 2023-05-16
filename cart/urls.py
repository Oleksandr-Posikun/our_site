from django.urls import path, include

from cart.views import ShopCart

obj = ShopCart.as_view()

urlpatterns = [
    path('', obj, name='cart'),
    path('mini_cart', obj, name='mini_cart'),
    path('add_cart', obj, name='add_cart'),
    path('del_cart', obj, name='del_cart'),
    path('add_cart/<int:count>', obj, name='add_cart_count'),
    ]
