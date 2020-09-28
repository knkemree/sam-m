from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ContactForm, LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from orders.models import Order
from products.models import Category, Product
from cart.forms import CartAddProductForm


def home_page(request):
    top_level_cats = Category.objects.filter(parent__isnull=True)
    area_rugs = Category.objects.filter(parent_id=18)
    bed_sheets = Product.objects.filter(category_id=17)
    towels = Product.objects.filter(category_id=19)
    cart_product_form = CartAddProductForm()
    context ={
        "title": "Hello world",
        "content": " This is Home page",
        'area_rugs': area_rugs,
        'bed_sheets': bed_sheets,
        'towels':towels,
        'top_level_cats': top_level_cats,
        'cart_product_form':cart_product_form
    }
    
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

