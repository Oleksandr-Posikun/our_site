import json

from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from store.models import Category, Product


class Base:
    def __init__(self):
        self.page = None
        self.product = Product.objects
        self.category = Category.objects
        self.all_product = self.product.all()
        self.all_category = self.category.all()
        self.context = {}

    def _filter_product(self, **kwargs):
        temp_dict = {}
        for key, value in kwargs.items():
            temp_dict[key] = self.product.filter(**{key: value})

        return temp_dict

    def _update_context(self, update_dict: dict):
        for key, value in update_dict.items():
            self.context[key] = value

        return True

    def _add_gallery(self, product):
        gallery = []
        product_images = list(product.images.all().values())
        for item in product_images:
            gallery.append(item['image'])

        return gallery

    def get_lens_category(self):
        temp_list = []

        for i in range(len(self.all_category)):
            len_product_dict = {'name': str(self.all_category[i]),
                                'count': int(Product.objects.filter(category_id=i + 1).count())}
            temp_list.append(len_product_dict)

        return temp_list


class Home(Base):
    def __init__(self):
        super().__init__()
        self.page = 'index.html'
        self.context = {'products': self.all_product, }
        self.__set_update_list_context = self._filter_product(popular=True, bestseller=True)
        self._update_context(self.__set_update_list_context)

    def index(self, request):
        return render(request, self.page, context=self.context)


class Store(Base):

    def __init__(self):
        super().__init__()
        self.page = 'shop.html'
        self.context = {'products': self.all_product, 'category': self.get_lens_category()}
        self.__set_update_list_context = self._filter_product(popular=True)
        self._update_context(self.__set_update_list_context)

    def shop(self, request):

        return render(request, self.page, context=self.context)


class Cart(Base):
    count_sums = []

    def __init__(self):
        super().__init__()

    @staticmethod
    def availability_in_cart(cart: list, product: dict):
        for i in cart:
            if i['id'] == product['id']:
                return i['id']

        return False

    @staticmethod
    def set_count_product(cart: list, product_id, count, subtraction=False,  price=0):
        if subtraction:
            for i in cart:
                if i['id'] == product_id:
                    i['count'] -= count
                    i['price'] -= price
                    if i['count'] == 0:
                        cart.remove(i)

                    return cart

        for i in cart:
            if i['id'] == product_id:
                i['count'] += count
                i['price'] += (price * count)

        return cart

    @staticmethod
    def get_all_count(cart: list):
        count = 0
        for i in cart:
            count += i['count']

        return count

    def sums_cart(self, obg: list):
        self.count_sums = 0
        for item in obg:
            self.count_sums += int(item['price'])

        return self.count_sums


class AjaxResponse(Base):
    cart = Cart()
    sums = 0
    count_product = 0

    def __init__(self):
        super().__init__()
        self.bad_request = "invalid request"
        self.__product_by_id = None
        self.cart_content = []

    def _check_ajax_value(self, request, get: str = '', id_product=True):
        is_ajax = request.headers.get('X-Request-With') == 'XMLHttpRequest'

        if not is_ajax:
            return HttpResponseBadRequest(self.bad_request)

        data = json.load(request)
        if id_product:
            product_id = data.get(get)
            return product_id

        return data

    def create_content(self, request, get: str = ''):
        product_id = self._check_ajax_value(request, get)
        self.__product_by_id = self._filter_product(id=product_id)
        product_list = self.__product_by_id[get].values().first()

        return product_list

    @csrf_exempt
    def ajax_quickview_popup(self, request):
        content = self.create_content(request, 'id')
        content['images'] = self._add_gallery(self.__product_by_id['id'][0])

        return JsonResponse(content)

    @csrf_exempt
    def ajax_mini_cart(self, request, count=1):
        if "mini_cart" not in str(request):
            cart_content = self.create_content(request, 'id')
            cart_content['count'] = count
            result = self.cart.availability_in_cart(self.cart_content, cart_content)

            if "add_cart" in str(request):
                if result:
                    self.cart_content = self.cart.set_count_product(self.cart_content, result, count,
                                                                    price=cart_content['price'])
                elif not result:
                    cart_content['price'] = cart_content['price'] * count
                    self.cart_content.append(cart_content)

            elif "del_cart" in str(request):
                self.cart_content = self.cart.set_count_product(self.cart_content, result, count,
                                                                subtraction=True,
                                                                price=cart_content['price'])

        self.sums = self.cart.sums_cart(self.cart_content)
        self.count_product = self.cart.get_all_count(self.cart_content)
        return JsonResponse({'data': self.cart_content, 'sums': self.sums, 'count_product': self.count_product})

    @csrf_exempt
    def ajax_sort(self, request):
        order = self._check_ajax_value(request, id_product=False)

        if order['sort'] != 'menu_order':
            cart_content = self.all_product.order_by(order['sort'])

        else:
            cart_content = self.all_product

        cart_content = serializers.serialize('json', cart_content)
        cart_content = json.loads(cart_content)

        return JsonResponse({'data': cart_content, 'sums': self.sums, 'count_product': self.count_product})
