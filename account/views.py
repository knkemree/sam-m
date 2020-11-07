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
from django.core.mail import send_mail





def registration_view(request):
    context = {}

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

            send_mail(
                'New Customer',
                'A new customer registered! ' +
                "Customer's e-mail address is {}".format(email),
                'emre@samnmtrade.com',
                ['emre@samnmtrade.com.com'],
                fail_silently=False,
            )


            return redirect('dashboard')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'register2.html', context)

