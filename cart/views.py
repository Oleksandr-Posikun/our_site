import json
import uuid

from django.db.models import Sum
from django.http import HttpResponseBadRequest, JsonResponse
from django.views import View

from cart.models import UserCart


# Create your views here.


class ShopCart(View):
    def __init__(self):
        super().__init__()
        self.model = UserCart
        self.data_cart_product = []
        self.url_mini_cart = "cart"
        self.add_cart = 'add_cart'
        self.del_cart = "del_cart"
        self.data = None
        self.user_id = None
        self.count_product = 0
        self.total_price = 0

    def post(self, request, count=1):
        is_ajax = request.headers.get('X-Request-With') == 'XMLHttpRequest'
        if not is_ajax:
            return HttpResponseBadRequest("invalid request")

        self.user_id = request.session.get('user_id')
        if self.user_id is None:
            self.user_id = str(uuid.uuid4())
            request.session['user_id'] = self.user_id

        check_request = str(request).replace('/', ' ')
        self.data = json.load(request)

        if self.add_cart in check_request:
            return self.add_cart_product(request, count)
        elif self.del_cart in check_request:
            return self.del_cart_product(request, count)
        elif self.url_mini_cart in check_request:
            return self.get_mini_cart(request)

    def get_mini_cart(self, request):
        user_cart = self.model.objects.filter(user=self.user_id)
        self.data_cart_product = []
        self.total_price = 0
        self.count_product = 0

        for cart_item in user_cart:
            product = cart_item.product
            img = product.image
            self.data_cart_product.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'image': str(img),
                'count': cart_item.count
            })
            self.total_price += cart_item.count * product.price
            self.count_product += cart_item.count

        self.total_price = str(round(self.total_price, 2))

        return JsonResponse({"data": self.data_cart_product,
                             'count_product': self.count_product,
                             'sums': self.total_price})

    def add_cart_product(self, request, count):
        product = self.model.objects.filter(user=self.user_id,  product_id=self.data['id']).values().first()
        if product:
            self.model.objects.filter(id=product['id']).update(count=product['count'] + count)
        else:
            self.model.objects.create(user=self.user_id, product_id=self.data['id'], count=count)

        return self.get_mini_cart(request)

    def del_cart_product(self, request, count):
        product = self.model.objects.filter(user=self.user_id, product_id=self.data['id']).values().first()

        self.model.objects.filter(id=product['id']).update(count=product['count'] - count)
        if product['count'] <= 1:
            self.model.objects.filter(id=product['id']).delete()

        return self.get_mini_cart(request)
