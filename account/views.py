from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegistrationForm
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from products.models import Category, Product
from account.models import Customers
import stripe




def registration_view(request):
    context = {}

    area_rugs = Category.objects.filter(parent_id=18)
    bed_sheets = Product.objects.filter(category_id=17)
    towels = Product.objects.filter(category_id=19)
    context = {'area_rugs': area_rugs,
                    'bed_sheets': bed_sheets,
                    'towels':towels,}
    if request.user.is_anonymous == False:
        return redirect('dashboard')

    elif request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")

            customer = Customers.objects.get(email=email)
            created_customer = stripe.Customer.create(
                description=email,
                email=email
            )
            customer.stripe_customer = created_customer.id
            customer.save()
            
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('dashboard')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'register2.html', context)

