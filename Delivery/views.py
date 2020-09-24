from django.shortcuts import redirect, render
from .forms import ShippingForm
from django.urls import reverse
from Delivery.models import Delivery_methods

# Create your views here.
def shipping_view(request): 
    context ={} 
    # create object of form 
    
    delivery_form = ShippingForm(request.POST)  
    # check if form data is valid 
    
    if delivery_form.is_valid(): 
        
        # save the form data to model 
        print("delivery formda ne var")
        delivery_method = delivery_form.cleaned_data["delivery_method"]
        delivery_instance = Delivery_methods.objects.get(delivery_method=delivery_method)
        request.session["delivery_id"] = delivery_instance.id
        
  
        context['delivery_form']= delivery_form
    else:
        #diyelim ki kullanici once delivery_method secti sonra selecti' secti' select secildiginde session'dan delivery_id silinmesi gerekiyor. aksi takdirde select secilmesine ragmen sag taraftaki cart ozetinde delivery method gozukuyor
        try:
            del request.session["delivery_id"]
        except:
            pass
    
    return redirect(reverse('orders:order_create'))
