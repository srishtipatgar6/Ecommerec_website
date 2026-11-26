
from django.shortcuts import render
from .models import Category, Product


def home(request):

    categories = Category.objects.all()

    products = Product.objects.all()

    featured_products = Product.objects.filter(
        is_featured=True
    )

    context = {
        'categories': categories,
        'products': products,
        'featured_products': featured_products,
    }

    return render(request, 'app1/home.html', context)


def about(request):
    return render(request, 'app1/about.html')


def contact(request):
    return render(request, 'app1/contact.html')
