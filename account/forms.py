from django import forms
from .models import Account
from django.contrib import messages

class RegistrationsForms(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
    }))

    confirms_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Your Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name' , 'last_name' , 'email' , 'phone_number' ,'password']
    def __init__(self , *args , **kwargs):
        # Input fields connect to html
        super(RegistrationsForms , self).__init__(*args , **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'

    def clean(self):
        clean_data = super(RegistrationsForms , self).clean()
        password = clean_data.get('password')
        confirms_password = clean_data.get('confirms_password')

        if password != confirms_password:
            raise forms.ValidationError(
                "password does't match!"
            )
