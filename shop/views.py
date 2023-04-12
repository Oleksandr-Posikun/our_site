from django.shortcuts import render

from .forms.subscribe import LoginForm, RegistrationForm
from .models import BestSeller, ProductPopular, StartSliders, StartBanners, OfferBanners, OurContactsInfo

# Create your views here.


def index(request):
    our_contacts = OurContactsInfo.objects.all()
    start_sliders = StartSliders.objects.all()
    offer_banners = OfferBanners.objects.all()
    product_popular = ProductPopular.objects.all()
    start_banners = StartBanners.objects.all()
    best_seller = BestSeller.objects.all()

    login_form = LoginForm()
    registration_form = RegistrationForm()

    if request.method == 'POST':
        subscribe_form_1 = LoginForm(request.POST)
        register_form_1 = RegistrationForm(request.POST)
        if subscribe_form_1.is_valid():
            print(subscribe_form_1.cleaned_data)
            subscribe_form_1 = LoginForm()

        if register_form_1.is_valid():
            print(register_form_1.cleaned_data)
            register_form_1 = RegistrationForm()

    return render(request, 'index.html',
                  {'start_slider': start_sliders.select_related('img'),
                   'offer_banners': offer_banners.select_related('img'),
                   'popular_products': product_popular.select_related('product', 'img'),
                   'start_banners': start_banners.select_related('img'),
                   'best_seller': best_seller.select_related('product', 'img'),
                   'our_contacts': our_contacts.values()[0],
                   'login_form': login_form,
                   'registration_form': registration_form}
                  )
