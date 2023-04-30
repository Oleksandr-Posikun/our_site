from django.urls import path, include

from store.views import Home, Shop

home = Home()
shop = Shop()

urlpatterns = [
    path('', home.index, name='home'),
    path('shop', shop.shop, name='shop'),
    path('ajax', home.ajax_response, name='ajax'),
    path('add_card/<int:id_product>', home.card, name=f'{home.add_card}'),
    path('del_card/<int:id_product>', home.card, name=f'{home.del_card}'),
]
