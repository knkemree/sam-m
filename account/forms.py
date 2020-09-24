
from django import forms  

from .models import Customers
#from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
#User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text= "Required. Add a valid email address", required=True)
    phone= PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': "e.g. +12107249073"}), required=False)
    class Meta:
        model = Customers
        #fields = UserCreationForm.Meta.fields + ('custom_field',)
        fields = ("email", "company_name", "first_name","last_name","phone","ein", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Customers.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is taken")
        return email


    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password2 != password:
            raise forms.ValidationError("Passwords must match!")
        return data

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        qs = Customers.objects.filter(phone=phone)
        if qs.exists():
            raise forms.ValidationError("Phone number already in use")
        if len(phone) == 10 and phone[0:2] != "+1":
            phone = "+12107249045"

        return phone    





