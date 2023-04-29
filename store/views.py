import json

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from store.models import Category, Product


class Home:
    def __init__(self):
        self.product = Product.objects
        self.user_card = []
        self.cart_sums = 0
        self.add_card = "add_card"  # check url for append product in card
        self.del_card = "del_card"  # check url for remove product from card

    @csrf_exempt
    def ajax_response(self, request):
        is_ajax = request.headers.get('X-Request-With') == 'XMLHttpRequest'

        if not is_ajax:
            return HttpResponseBadRequest("invalid request")

        data = json.load(request)
        product_id = data.get('id')
        product = self.product.filter(id=product_id)
        product_list = product.values().first()
        product_list['images'] = self.add_gallery(product[0])

        return JsonResponse(product_list)

    def add_gallery(self, product):
        gallery = []
        product_images = list(product.images.all().values())

        for item in product_images:
            gallery.append(item['image'])

        return gallery

    def index(self, request):
        products = self.product.all()
        popular = self.product.filter(popular=True)
        bestseller = self.product.filter(bestseller=True)

        return render(request,
                      'index.html',
                      {
                          'products': products,
                          'popular': popular,
                          'bestseller': bestseller,
                          'user_card': self.user_card,
                          'cart_sums': self.cart_sums
                      }
                      )

    def card(self, request, id_product):
        todo_request = str(request)
        product = self.product.filter(id=id_product).values().first()

        if self.del_card in todo_request:
            self.cart_sums = self.cart_sums - product['price']
            self.user_card.remove(product)

            return HttpResponseRedirect('/')
        elif self.add_card in todo_request:
            self.user_card.append(product)
            self.cart_sums = self.cart_sums + product['price']

            return HttpResponseRedirect('/')


class Shop:
    def __init__(self):
        self.product = Product.objects

    def shop(self, request):
        products = self.product.all()
        return render(request, 'shop.html', {'products': products})
