from email import message
from tkinter import Button
from urllib import request
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError
from django.shortcuts import redirect
from .models import BillingAddress, OrderItem

from ESite_App.models import ShippingAddress

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()
    email2 = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['email']


    def clean(self):
        cleaned_data = super(UpdateUserForm, self).clean()
        email = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")  
          
        if email != email2:
            self.add_error('email2', "Email does not match")








class UpdatePassword(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    Enter_Your_Password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
      
        model = User
        fields = ['password']


    def clean(self):
        cleaned_data = super(UpdatePassword, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")  
          
        if password2 != password:
            self.add_error('password', "Passwords does not match")




class ShippingAddressForm(forms.ModelForm):

    class Meta:

        model = ShippingAddress
        exclude =['user']

        
class BillingAddressForm(forms.ModelForm):

    class Meta:

        model = BillingAddress
        exclude =['user' 'user_id']
        db_table = 'ecommerce.esite_app_billingaddress'
        fields = ['first_name','last_name','company', 'city', 'zipcode', 'address', 'phone_number']



class UpdateUserAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        exclude =['user']
        db_table = 'e-commerce.esite_app_shippingaddress'
