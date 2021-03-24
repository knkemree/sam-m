from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.storage import FileSystemStorage
from .forms import ContactForm, LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from orders.models import Order
from products.models import Category, Product
from cart.forms import CartAddProductForm

from django.contrib.auth.views import LoginView as DefaultLoginView
from django.views.generic import CreateView
from marketing.models import Slider
from products.forms import SearchForm

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
                if valuenext == "http://127.0.0.1:8000/logout/" or valuenext == "http://127.0.0.1:8000/login/" or valuenext == 'https://msrugs.com/login/' or valuenext == 'https://msrugs.com/logout/' or valuenext == 'https://samnmtrade.com/login/' or valuenext == 'https://samnmtrade.com/logout/' :
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
    sliders = Slider.objects.filter(active=1)
    top_level_cats = Category.objects.filter(parent__isnull=True, active=1).select_related('parent')
    
    print(top_level_cats)
    search_form = SearchForm()
    try:
        area_rug = Category.objects.get(slug__contains="area-rugs")
        area_rugs = Category.objects.filter(parent_id=area_rug.id, active=1).select_related('parent')
    except:
        area_rugs = []
    
    try:
        bed_sheet = Category.objects.get(slug__contains="bed-sheets")
        bed_sheets = Product.objects.filter(category_id=bed_sheet.id)[:10].select_related('category')
    except:
        bed_sheets = []

    try:
        towel = Category.objects.get(slug__contains="towel")
        towels = Product.objects.filter(category_id=towel.id)[0:10].select_related('category')
    except:
        towels= []
    
    cart_product_form = CartAddProductForm()
    context ={
        'area_rugs': area_rugs,
        'bed_sheets': bed_sheets,
        'towels':towels,
        'top_level_cats': top_level_cats,
        'cart_product_form':cart_product_form,
        'search_form':search_form,
        'sliders':sliders,
    }
    
    return render(request, "home_page.html", context)

def about_page(request):
    context = {
        "title": "About Page",
        "content": " This is about us page"
    }
    return render(request, "about.html", context)

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
def dashboard(request, order_id=None):

    user_orders = Order.objects.filter(email=request.user)

    user = request.user
    
    

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request,
                  'dashboard.html',
                  {'section': 'dashboard',
                  'user_orders':user_orders,
                  'user':user,
                  'form':form,
                  })

@login_required
def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'order_details.html', context)


def tee(request):
    return render(request, 'tee/tee.html')

