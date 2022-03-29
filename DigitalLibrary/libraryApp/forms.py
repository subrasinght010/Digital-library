from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('G', 'Gpay'),
    ('P', 'Paytm')
)
class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(required=True,label = 'Please Enter Your Password' ,widget = forms.PasswordInput(attrs=
    {'class':'form', 'placeholder':'********'}))
    password2 = forms.CharField(required=True,label = 'Please Confrim Your Password' ,widget = forms.PasswordInput(attrs=
    {'class':'form', 'placeholder':'********'}))
    email = forms.CharField(required=True,label = 'Please Enter Your Email Address', widget = forms.EmailInput(attrs=
    {'class':'form', 'placeholder':'abc@gmail.com'}))
    username = forms.CharField(required=True,label = 'Please Enter Your Username',  widget = forms.TextInput(attrs={'class':'form', 'placeholder':'username'}))

    class Meta:
        """docstring for Meta."""
        model = User
        fields = ['username','email','password1','password2',]

class LoginForm(AuthenticationForm):
    """docstring for LogiForm."""
    username = UsernameField(required=True,label='Enter Your username',widget=forms.TextInput(attrs={'autofocus':'true','class':'form', 'placeholder':'username'}))
    password =forms.CharField(required=True,label='Enter Your Password',strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form', 'placeholder':'********'}))

"""class PasswordchangeForm(PasswordChangeForm):
    docstringforPasswordchangeForm.
    password1 = forms.CharField(required=True,help_text=password_validation,label = 'Please Enter Your New Password' ,widget = forms.PasswordInput(attrs=
    {'class':'form', 'placeholder':'********'}))
    password2 = forms.CharField(required=True,label = 'Please Confrim Your Password' ,widget = forms.PasswordInput(attrs=
    {'class':'form', 'placeholder':'********'}))"""


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    State_Name = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(required=False,widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100',}))
    shipping_zip = forms.CharField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
