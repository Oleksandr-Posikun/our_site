from django.urls import path, include

from shop.views import ShopHome, AjaxData

urlpatterns = [
    path('', ShopHome.as_view(), name='shop'),
    path('sort', AjaxData.as_view(), name='sort'),
]
