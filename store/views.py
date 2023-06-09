import json
import os

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import ListView, View

from store.models import Product


class HomePage(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular'] = self.model.objects.filter(popular=True)
        context['bestseller'] = self.model.objects.filter(bestseller=True)

        return context


class AjaxData(View):
    def _add_gallery(self, product):
        gallery = []
        product_images = list(product.images.all().values())
        for item in product_images:
            gallery.append(item['image'])

        return gallery

    def post(self, request):
        is_ajax = request.headers.get('X-Request-With') == 'XMLHttpRequest'

        if not is_ajax:
            return HttpResponseBadRequest("invalid request")

        data = json.load(request)
        product = Product.objects.filter(id=data['id'])
        content = product.values().first()
        content['images'] = self._add_gallery(product[0])

        return JsonResponse(content)
