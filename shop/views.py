import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.views import View
from django.views.generic import ListView
from store.models import Category, Product
from django.core import serializers
import os

# Create your views here.


class ShopHome(ListView):
    paginate_by = 6
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular'] = Product.objects.filter(popular=True)
        categories = Category.objects.all()
        for category in categories:
            product_count = Product.objects.filter(category=category).count()
            category.count = product_count

        context['categories'] = categories

        return context


class AjaxData(View):
    model = Product

    def post(self, request):
        is_ajax = request.headers.get('X-Request-With') == 'XMLHttpRequest'

        if not is_ajax:
            return HttpResponseBadRequest("invalid request")

        data = json.load(request)
        if data['sort'] != 'menu_order':
            cart_content = self.model.objects.all().order_by(data['sort'])
        else:
            cart_content = self.model.objects.all()

        cart_content = serializers.serialize('json', cart_content)
        cart_content = json.loads(cart_content)

        return JsonResponse({'data': cart_content})
