from django.shortcuts import render, get_object_or_404
from store.models import Product
from sub_categories.models import SubCategory

def store(request, sub_category_slug=None):
    if sub_category_slug is not None:
        sub_category = get_object_or_404(SubCategory, slug=sub_category_slug)
        products = Product.objects.filter(sub_category=sub_category, is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.filter(is_available=True)
        products_count = products.count()

    context = {
        'products': products,
        'product_count': products_count,
    }

    return render(request, "store/store.html", context)

def product_details(request , sub_category_slug ,product_slug ):
    try:
        single_product = Product.objects.get(sub_category__slug = sub_category_slug , slug = product_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_product':single_product,
    }

    return render(request , "store/product_details.html" , context)
