from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ContactForm, LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from orders.models import Order
from products.models import Category


def home_page(request):
    categories = Category.objects.all()
    context ={
        "title": "Hello world",
        "content": " This is Home page",
        'categories': categories
    }
    if request.user.is_authenticated:
        context["premium_content"] = "YEAAAHHH" 
    return render(request, "home_page.html", context)

def about_page(request):
    context = {
        "title": "About Page",
        "content": " This is about us page"
    }
    return render(request, "home_page.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Page",
        "content": " This is contact page",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    #if request.method=="POST":
        #print(request.POST.get("Company_name"))
        #print(request.POST)
    
    return render(request, "contact/view.html", context)







@login_required
def dashboard(request):
    return render(request,
                  'dashboard.html',
                  {'section': 'dashboard'})

