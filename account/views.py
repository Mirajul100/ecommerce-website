from django.shortcuts import render , redirect
from .forms import RegistrationsForms
from .models import Account
from django.contrib import messages , auth
from .forms import RegistrationsForms
from django.contrib.auth.decorators import login_required

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
            messages.success(request , "Registration Successful")
            return redirect('register')

    else:
        form = RegistrationsForms()
        
    context= {
        'form':form,
    }
    return render (request , 'accounts/register.html' , context)

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
            return redirect('login')


    return render (request , 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    try:
        auth.logout(request)
        messages.success(request , 'Your Logged Out Successfully')
        return redirect('login')
    except:
        pass

