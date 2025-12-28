from django.shortcuts import render , redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order
import datetime
from decimal import Decimal
from website import settings
from decimal import Decimal
from sslcommerz_python_api import SSLCSession

def payment(request):
    if settings.SSLCOMMERZ_SANDBOX:
        store_id = settings.SSLCOMMERZ_STORE_ID
        store_pass = settings.SSLCOMMERZ_STORE_PASS

        mypayment = SSLCSession(
            sslc_is_sandbox=True,
            sslc_store_id=store_id,
            sslc_store_pass=store_pass
            )
        mypayment.set_urls(
            success_url='example.com/success',
            fail_url='example.com/failed',
            cancel_url='example.com/cancel',
            ipn_url='example.com/payment_notification'
            )
        pass
    else:
        pass
    return render(request , 'orders/payment.html')

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