from django import forms
from .models import Account , UserProfile
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

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number' , 'email')
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-group'


class UserProfileForm(forms.ModelForm):

    # Remove the default profile_picture url
    profile_picture = forms.ImageField(
        required=False,  # optional
        widget=forms.FileInput(attrs={
            'class': 'form-control'  # optional CSS class
        })
    )
    class Meta:
        model = UserProfile
        fields = ('profile_picture','address_line_1','address_line_2','country','city','state')

