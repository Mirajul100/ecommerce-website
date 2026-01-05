from django.shortcuts import render , redirect
from .forms import RegistrationsForms , UserForm , UserProfileForm
from .models import Account , UserProfile
from django.contrib import messages , auth
from .forms import RegistrationsForms
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404

from carts.models import Cart , CartItem
from carts.views import _cart_id
from carts.views import checkout
from orders.models import Order , OrderProduct

# Email Verification 

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes , force_str
from django.contrib.auth.tokens import default_token_generator
import requests

def register(request):

    if request.method == 'POST':
        form = RegistrationsForms(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'].title()
            last_name = form.cleaned_data['last_name'].title()
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user_name = email.split("@")[0]
            user = Account.objects.create_user(first_name= first_name,
                                               last_name= last_name,
                                               email= email,
                                               user_name = user_name,
                                               password=password)
            user.phone_number = phone_number
            user.save()

            # User verification
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account'
            message = render_to_string('account/activation_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })

            to_email = email
            send_mail = EmailMessage(mail_subject , message , to=[to_email])
            send_mail.send()
            # messages.success(request , 'Registration successful! Please check your email to activate your account.')
            return redirect(reverse('login')+'?command=verification&email='+email)
        

    else:
        form = RegistrationsForms()
        
    context= {
        'form':form,
    }
    return render (request , 'account/register.html' , context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email , password=password) 

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart= cart).exists()

                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variation by cart id
                    product_variation =[]
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variation
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []

                    for item in cart_item:
                        ex_variation = item.variations.all()
                        ex_var_list.append(list(ex_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id= item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            # This is return to user visited page
            auth.login(request , user)
            messages.success(request , 'Your Logged In Successfully')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:
                return redirect('dashboard')
        
        else:
            messages.error(request , 'Invalid Login Credential')
            return redirect('register')


    return render (request , 'account/login.html')

@login_required(login_url='login')
def logout(request):
    try:
        auth.logout(request)
        messages.success(request , 'Your Logged Out Successfully')
        return redirect('login')
    except:
        pass

def activate(request , uidb64 , token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account._default_manager.get(pk=uid)
    except(ValueError , TypeError , OverflowError , Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user , token):

        user.is_active = True
        user.save()
        messages.success(request , 'Congratulation! Your account is activated')
        return redirect('login')
    else:
        messages.error(request , 'Your Account is invalid')
        return redirect('register')
    

@login_required(login_url='login')
def dashboard(request):
    return render(request , 'account/dashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('account/reset_password_email.html' , {
                'user':user,
                'domain':current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject , message , to=[to_email])
            send_email.send()

            messages.success(request , 'Password reset email has been send to your account')
            return redirect('login')
        else:
            messages.error(request , 'Account Does not exits')
            return redirect('forgot_password')
        
    return render(request , 'account/forgot_pass.html')

def reset_password_valid(request , uidb64 , token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account._default_manager.get(pk=uid)
    except(ValueError , TypeError , OverflowError , Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user , token):
        request.session['uid'] = uid
        messages.success(request , 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request , 'This link has been expired')
        return redirect('login')
        
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request , 'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request , 'Password do not match')
            return redirect('reset_password')
        
    else:
        return render(request , 'account/reset_password.html')
    
def product_history(request):
    order = Order.objects.filter(user=request.user , is_ordered=True).order_by('-created_at')
    order_product = OrderProduct.objects.filter(order__in=order)
    context = {
        'order_product':order_product,
    }
    return render(request , 'account/product_history.html' , context)

def edit_profile(request):
    user_profile , create = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST , instance=request.user)
        profile_form = UserProfileForm(request.POST , request.FILES , instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request , 'Your Profile Hax Been Updated')
            return redirect('edit_profile')
        
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'user_profile':user_profile,
    }
    
    return render(request , 'account/edit_profile.html' , context)