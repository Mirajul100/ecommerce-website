from django.shortcuts import render , redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order , Payment , OrderProduct
from django.conf import settings
from decimal import Decimal
from sslcommerz_python_api import SSLCSession
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from account.models import Account
from django.contrib import messages
from store.models import Product

import datetime

def payment(request, order_number):
    order = Order.objects.get(user=request.user, order_number=order_number, is_ordered=False)

    sslc = SSLCSession(
        sslc_is_sandbox=settings.SSLCOMMERZ_SANDBOX,
        sslc_store_id=settings.SSLCOMMERZ_STORE_ID,
        sslc_store_pass=settings.SSLCOMMERZ_STORE_PASS
    )

    sslc.set_urls(
        success_url=request.build_absolute_uri(reverse('payment_success')),
        fail_url=request.build_absolute_uri(reverse('payment_failed')),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
        ipn_url=request.build_absolute_uri(reverse('payment_ipn')),
    )

    # Payment information
    sslc.set_product_integration(
        total_amount=Decimal(order.order_total),
        currency='BDT',
        product_category='Ecommerce',
        product_name='Clouts',
        num_of_item=1,
        shipping_method='Courier',
        product_profile='general',
    )

    # Customer info
    sslc.set_customer_info(
        name=f"{order.first_name} {order.last_name}",
        email=order.email,
        address1=order.address_line_1,
        address2=order.address_line_2,
        city=order.city,
        postcode='1200',
        country=order.country,
        phone=order.phone
    )

    # Shipping info
    sslc.set_shipping_info(
        shipping_to=f"{order.first_name} {order.last_name}",
        address=order.address_line_1,
        city=order.city,
        postcode='1200',
        country=order.country
    )

    sslc.set_additional_values(
        value_a=str(request.user.id),
        value_b=str(order.id)
    )


    response = sslc.init_payment()

    if response.get('status') == 'SUCCESS':
        return redirect(response['GatewayPageURL'])

    return redirect('checkout')

@ csrf_exempt
def payment_success(request):

    if request.method == "POST":

        tran_id = request.POST.get('tran_id')
        payment_method = request.POST.get('card_type')
        amount = request.POST.get('amount')
        status = request.POST.get('status')
        user_id = request.POST.get('value_a')
        order_id = request.POST.get('value_b')

        if not tran_id or not user_id:
            return render(request, 'orders/pay_fail.html')

        # Check payment is valid 
        if status != "VALID":
            return render(request, 'orders/pay_fail.html')

        try:
            user = Account.objects.get(id=user_id)
        except Account.DoesNotExist:
            return render(request, 'orders/pay_fail.html')
        
        try:
            order = Order.objects.get(id=order_id , user=user , is_ordered=False)
        except Order.DoesNotExist:
            return render(request, 'orders/pay_fail.html')
        
        if not Payment.objects.filter(payment_id=tran_id).exists():
            payment = Payment(
                user=user,
                payment_id=tran_id,
                payment_method=payment_method,
                amount_paid=amount,
                status=status,
            )
            payment.save()
            order.payment = payment
            order.is_ordered = True
            order.status = 'Accepted'
            order.save()

        messages.success(request , "Payment Successful")
        return redirect('order_completed' , order_number=order.order_number)

    return render(request, 'orders/pay_fail.html')


@ csrf_exempt
def payment_failed(request):
    return render(request , 'orders/pay_fail.html')

@ csrf_exempt
def payment_cancel(request):
    return HttpResponse("Payment Cancelled")

@csrf_exempt
def payment_ipn(request):
    return HttpResponse("IPN Received")

def order_completed(request , order_number):
    order = Order.objects.get(order_number=order_number)
    cart_items = CartItem.objects.filter(user=order.user)

    # Mode cart item to database
    for item in cart_items:
        order_product = OrderProduct(
            user=order.user,
            order=order,
            payment=order.payment,
            product=item.product,
            quantity=item.quantity,
            product_price=item.product.price,
            ordered=True,
        )
        order_product.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variations.set(product_variation)
        order_product.save()

        # Reduce the quantity of ordered product
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Deleted the user cart item
    cart_items.delete()



    context = {
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'orders/order_completed.html', context)

def place_order(request, total=0, quantity=0):
    shipping = 40
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    if cart_items.count() <= 0:
        return redirect('store')

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax + shipping

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            today = datetime.date.today()
            current_date = today.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user , is_ordered=False , order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }

            return render(request , 'orders/payment.html' , context)

        else:
            return redirect('checkout')