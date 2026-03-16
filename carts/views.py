from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from store.models import Product , Variation
from .models import Cart , CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account import forms

def _cart_id(request):

    cart = request.session.session_key

    if not cart :
        cart = request.session.create()
    return cart

def add_cart(request , product_id):

    current_user = request.user
    product = Product.objects.get(id= product_id)

    if current_user.is_authenticated:
        product_variation = []

        # This code add color and size also brand
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
        
                try:
                    variation = Variation.objects.get(product= product , variation_category__iexact=key , variation_value__iexact=value)
                    product_variation.append(variation)

                except:
                    pass

        is_cart_item_exits = CartItem.objects.filter(product= product , user=current_user).exists()

        if is_cart_item_exits:
            cart_item = CartItem.objects.filter(product=product ,user=current_user)

            # -- Logic --
            # existing_variations --> database
            # current_variations --> product_variation
            # item_id --> database

            ex_var_list = []
            id = []

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item

                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product = product , id = item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product , quantity=1 , user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)

                    # cart_item.quantity += 1
                item.save()

        else:
            
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user=current_user,
            )
            
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()

        return redirect ("cart")
    
    # User is Not authenticated
    else:

        product_variation = []

        # This code add color and size also brand
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
        
                try:
                    variation = Variation.objects.get(product= product , variation_category__iexact=key , variation_value__iexact=value)
                    product_variation.append(variation)

                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id= _cart_id(request)) # get the cart using the cart_id
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request),
            )
        cart.save()

        is_cart_item_exits = CartItem.objects.filter(product= product , cart=cart).exists()

        if is_cart_item_exits:
            cart_item = CartItem.objects.filter(product=product ,cart=cart)

            # -- Logic --
            # existing_variations --> database
            # current_variations --> product_variation
            # item_id --> database

            ex_var_list = []
            id = []

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item

                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product = product , id = item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product , quantity=1 , cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)

                    # cart_item.quantity += 1
                item.save()

        else:
            
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()

        return redirect ("cart")

def remove_cart(request , product_id , cart_item_id):
    product = get_object_or_404(Product , id = product_id)
    user = request.user

    try:
        if user.is_authenticated:
            cart_item = CartItem.objects.get(product=product , user= user , id=cart_item_id)

        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product , cart= cart , id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')

def remove_cart_item(request , product_id , cart_item_id):
    product = get_object_or_404(Product , id = product_id)
    user = request.user
    
    if user.is_authenticated:
        cart_item = CartItem.objects.get(product=product , user=user , id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product , cart=cart , id=cart_item_id)
    
    cart_item.delete()

    return redirect('cart')

def cart(request , total=0 ,quantity=0 , cart_items= None):
    try:
        tax = 0
        grand_total = 0
        shipping = 40
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user , is_active = True)

        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart , is_active = True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity )
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = tax + total + shipping
    
    except ObjectDoesNotExist:
        pass
    

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }

    return render(request , 'store/cart.html' , context)

@login_required(login_url='login')
def checkout(request , total=0 , quantity=0 , cart_items = None):
    try:
        user_profile , create = forms.UserProfile.objects.get_or_create(user=request.user)
        user_profile_form = forms.UserProfileForm(instance=user_profile)
        user_form = forms.UserForm(instance=request.user)
        tax = 0
        shipping = 40
        grand_total = 0
        user = request.user
        if user.is_authenticated:
            cart_items = CartItem.objects.filter(user=user , is_active = True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart , is_active = True)
            product = Product.objects.get(id= _cart_id)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            if cart_item.quantity > cart_item.product.stock:
                messages.error(request, f'Not enough stock for {cart_item.product} please check the stock first')
                return redirect('cart')

        tax = (2 * total) / 100
        grand_total = total + tax + shipping

    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        'user_form': user_form,
        'user_profile_form':user_profile_form,
    }

    return render(request , 'store/checkout.html' , context)