from django.shortcuts import render , redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order
import datetime
from django.conf import settings
from decimal import Decimal
from sslcommerz_python_api import SSLCSession
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


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

    response = sslc.init_payment()

    if response.get('status') == 'SUCCESS':
        return redirect(response['GatewayPageURL'])

    return redirect('checkout')

@ csrf_exempt
def payment_success(request):
    current_user = request.user
    context={
        'current_user':current_user,
    }
    return render(request , 'orders/pay_success.html' , context)

@ csrf_exempt
def payment_failed(request):
    return render(request , 'orders/pay_fail.html')

@ csrf_exempt
def payment_cancel(request):
    return HttpResponse("Payment Cancelled")

@csrf_exempt
def payment_ipn(request):
    return HttpResponse("IPN Received")


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