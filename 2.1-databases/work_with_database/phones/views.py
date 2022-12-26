from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_type = request.GET.get('sort', 'name')
    phones_objects = Phone.objects.all()

    if sort_type == 'name':
        phones_objects = phones_objects.order_by('name')
    elif sort_type == 'min_price':
        phones_objects = phones_objects.order_by('price')
    elif sort_type == 'max_price':
        phones_objects = phones_objects.order_by('price').reverse()

    context = {'phones': phones_objects
               }

    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone_object = Phone.objects.get(slug=slug)

    context = {'phone': phone_object
               }
    return render(request, template, context)
