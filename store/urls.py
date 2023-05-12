from django.urls import path, include

from store.views import HomePage, AjaxData


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('ajax', AjaxData.as_view(), name='ajax'),
]

# urlpatterns = [
    # path('', home.index, name='home'),
    # path('ajax', ajax.ajax_quickview_popup, name='ajax'),
    # path('add_cart', ajax.ajax_mini_cart, name='add_cart'),
    # path('del_cart', ajax.ajax_mini_cart, name='del_cart'),
    # path('mini_cart', ajax.ajax_mini_cart, name='mini_cart'),
    # path('add_cart/<int:count>', ajax.ajax_mini_cart, name='add_cart'),
    # path('sort', ajax.ajax_sort, name='sort'),
    # path('shop', shop.shop, name='shop'),

# ]
