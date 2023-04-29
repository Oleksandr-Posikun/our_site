from django.urls import path, include

from store.views import Home, Shop

home = Home()
shop = Shop()

urlpatterns = [
    path('', home.index, name='home'),
    path('ajax', home.ajax_response, name='ajax'),
    path('card/<int:id_product>', home.card, name='add_card'),
    path('del_card/<int:id_product>', home.card, name='del_card'),
    path('shop', shop.shop, name='shop'),
]
