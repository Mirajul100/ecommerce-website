from django.shortcuts import render, get_object_or_404
from store.models import Product
from sub_categories.models import SubCategory
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import PageNotAnInteger , EmptyPage , Paginator
from django.db.models import Q
from .models import ProductGallery

def store(request, sub_category_slug=None):
    if sub_category_slug is not None:
        sub_category = get_object_or_404(SubCategory, slug=sub_category_slug)
        products = Product.objects.filter(sub_category=sub_category, is_available=True)
        paginator = Paginator(products , 4)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products , 4)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        products_count = products.count()

    context = {
        'products': page_products,
        'product_count': products_count,
    }

    return render(request, "store/store.html", context)

def product_details(request , sub_category_slug ,product_slug ):
    try:
        single_product = Product.objects.get(sub_category__slug = sub_category_slug , slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request) , product= single_product).exists()

    except Exception as e:
        raise e
    
    # Get product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product':single_product,
        'in_cart':in_cart,
        'product_gallery':product_gallery,
    }

    return render(request , "store/product_details.html" , context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-modify_date').filter(Q(description__icontains=keyword) | 
                                                                       Q(product_name__icontains=keyword) | 
                                                                       Q(sub_category__sub_category_name__icontains=keyword) |
                                                                       Q(category__Category_name__icontains=keyword))
            products_count = products.count()

    context = {
        'products': products,
        'products_count':products_count,
    }

    return render(request , "store/store.html" , context)