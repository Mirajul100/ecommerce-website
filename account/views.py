from django.shortcuts import render , redirect
from .forms import RegistrationsForms
from .models import Account
from django.contrib import messages , auth
from .forms import RegistrationsForms
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.urls import reverse

# Email Verification 

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes , force_str
from django.contrib.auth.tokens import default_token_generator

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
            auth.login(request , user)
          # messages.success(request , 'Your Logged In Successfully')
            return redirect('home')
        
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