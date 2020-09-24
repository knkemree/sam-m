from django import forms
from django.contrib.auth.models import User



class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "id":"form_full_name", "placeholder":"Your fullname"}))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "id":"form_full_name", "placeholder":"Your email address"}))
    ein_number = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "type":"number", "placeholder":"Your EIN #"}))
    
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "id":"form_full_name", "placeholder":"Your message..."}))

    def clean_ein_number(self):
        ein = self.cleaned_data.get("ein_number")
        if len(ein) != 9:
            raise forms.ValidationError("EIN has to be nine-digit number")
        return ein

    def clean_fullname(self):
        fullname = self.cleaned_data.get("fullname").title()
        if not ' ' in fullname:
            raise forms.ValidationError("There has to be a space between your first name and last name")
        return fullname

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if not "@" in email:
            raise forms.ValidationError("Please enter valid e-mail")
        return email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is taken")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password2 != password:
            raise forms.ValidationError("Passwords must match!")
        return data


