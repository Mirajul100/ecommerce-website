from .models import Cart , CartItem
from .views import _cart_id

def count(request):
    cart_count = 0

    if 'admin' in request.path:
        return {}
    
    else:

        cart = Cart.objects.filter(cart_id = _cart_id(request))
        try:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.all().filter(user=request.user)
            else:
                cart_item = CartItem.objects.all().filter(cart = cart[:1])
                
            for cart_items in cart_item:
                cart_count += cart_items.quantity

        except Cart.DoesNotExist:
            cart_count = 0
    
    return dict(cart_count = cart_count)

