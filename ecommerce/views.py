from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ContactForm, LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from orders.models import Order
from products.models import Category, Product
from cart.forms import CartAddProductForm

from django.contrib.auth.views import LoginView as DefaultLoginView
from django.views.generic import CreateView

def login_form(request):
       #buranin ismini login koyma
    valuenext= request.META.get('HTTP_REFERER')
    print("valuenext!!!!!!")
    print(valuenext)
    context2 = {"valuenext":valuenext}
    
    print(request.session.get("nexti"))
    if request.method == 'POST':
        
        next_url = request.POST['next'] 
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if valuenext:
                if valuenext == "http://127.0.0.1:8000/logout/" or valuenext == "http://127.0.0.1:8000/login/" or valuenext == 'https://msrugs.com/login/' or valuenext == 'https://msrugs.com/logout/' :
                    return redirect('/')
                return redirect(next_url)
                #return redirect(next_url) #next url varsa next url'ye yonlendirir
            else:
                HttpResponse("Sam & M")
            #redirect to a success page
                return redirect('/') #next url yoksa anasayfaya yonlendirir
            # HTTP response(user.username)
        else:
            context = {'error': 'The e-mail address or password you entered was incorrect.',
                       }
            # return an 'invalid login' error message
            return render(request, "registration/login.html", context)
    
    return render(request, "registration/login.html", context2)


def home_page(request):
    
    
    top_level_cats = Category.objects.filter(parent__isnull=True)
    
    try:
        area_rug = Category.objects.get(slug__contains="area-rugs")
        area_rugs = Category.objects.filter(parent_id=area_rug.id)
    except:
        area_rugs = []
    
    try:
        bed_sheet = Category.objects.get(slug__contains="bed-sheets")
        bed_sheets = Product.objects.filter(category_id=bed_sheet.id)
    except:
        bed_sheets = []
    print("bed_sheets")
    print(bed_sheets)

    try:
        towel = Category.objects.filter(slug__contains="towels")
        towels = Product.objects.filter(category_id=towel.id)
    except:
        towels= []

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
    area_rugs = Category.objects.filter(parent_id=18)
    bed_sheets = Product.objects.filter(category_id=17)
    towels = Product.objects.filter(category_id=19)
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Page",
        "content": " This is contact page",
        "form": contact_form,
        'area_rugs': area_rugs,
                    'bed_sheets': bed_sheets,
                    'towels':towels,
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

