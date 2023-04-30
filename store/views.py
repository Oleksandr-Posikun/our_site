import json

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from store.sorted import UserSort
from store.models import Category, Product


class Base:
    sorted_form = UserSort()
    option = None
    user_card = []
    cart_sums = []

    def __init__(self):
        self.product = Product.objects
        self.add_card = "add_card"  # check url for append product in card
        self.del_card = "del_card"  # check url for remove product from card

    def card(self, request, id_product):
        todo_request = str(request)
        product = self.product.filter(id=id_product).values().first()
        next_url = request.GET.get('next', '/')

        if self.del_card in todo_request:
            self.cart_sums.remove(product['price'])
            self.user_card.remove(product)

            return redirect(next_url)

        elif self.add_card in todo_request:
            self.user_card.append(product)
            self.cart_sums.append(product['price'])

            return redirect(next_url)


class Home(Base):
    def __init__(self):
        super().__init__()

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
                          'cart_sums': sum(self.cart_sums)
                      }
                      )


class Shop(Base):
    def __init__(self):
        super().__init__()

    def shop(self, request):
        popular = self.product.filter(popular=True)
        user_sort = UserSort(request.POST or None, initial={'frameworks': request.session.get('frameworks')})

        if user_sort.is_valid():
            option = user_sort.cleaned_data['frameworks']
            products = self.product.all().order_by(option)
            request.session['frameworks'] = option
        elif self.option is not None:
            products = self.product.all().order_by(self.option)
        else:
            products = self.product.all()

        return render(request,
                      'shop.html',
                      {
                          'products': products,
                          'populars': popular,
                          'user_card': self.user_card,
                          'cart_sums': sum(self.cart_sums),
                          'sort': self.sorted_form
                      }
                      )
