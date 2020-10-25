from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product, Variation
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from coupons.models import Campaign
from Delivery.models import Delivery_methods
from django.http import HttpResponseRedirect
from django.contrib import messages

import requests
import http.client
import mimetypes
import json



@require_POST
def cart_add(request, product_id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart(request)
    form = CartAddProductForm(request.POST)

    if form.is_valid():

        cd = form.cleaned_data

        if cd['override'] == True :
           product = get_object_or_404(Variation, id=product_id) #bunu product detail sayfasinda kullaniyor
        else:
           product = get_object_or_404(Variation, id=product_id)  #bunu cart detail sayfasini guncellerken kullaniyor
        
        conn = http.client.HTTPSConnection("ecomdash.azure-api.net")
        payload = ''
        headers = {
            'Ocp-Apim-Subscription-Key': 'ce0057d8843342c8b3bb5e8feb0664ac',
            'ecd-subscription-key': '0e26a6d3e46145d5b7dd00a9f0e23c39'
        }
        conn.request("GET", "/api/Inventory?Type=Product&Id="+str(int(float(product.ecomdashid))), payload, headers)
        res = conn.getresponse()
        data = res.read()
        veri1 = json.loads(data.decode("utf-8"))
        #print(veri1)
        #print(veri1["data"])
        on_hand = int(veri1["QuantityOnHand"])
        print("on hand burda")
        print(type(on_hand), on_hand)
        
        cart.add(
                 product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        

        

    else:
        del request.session["variation_id"]
    
    try:
        campaign = Campaign.objects.get(active=1, amount_from__lte=cart.get_total_price(),amount_to__gte=cart.get_total_price())
        request.session["campaign_id4"]=campaign.id
    except: 
        pass

    for key, value in request.session.items():
        if key == "cart":

            print('{} => {}'.format(key, value))
            for k, v in value.items():
                if str(product.id) == str(k):

                    if v["quantity"] > int(on_hand):
                        
                        v["quantity"] = int(on_hand)
                        messages.warning(request, "Reached max. quantity")
                    elif cd['override'] == True:
                        messages.success(request, "Cart updated...")
                    else:
                        messages.success(request, "Added to cart !")


    return HttpResponseRedirect(url)
    #return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart(request)
    product = get_object_or_404(Variation, id=product_id)
    cart.remove(product)
    try:
        campaign = Campaign.objects.get(active=1, amount_from__lte=cart.get_total_price(),amount_to__gte=cart.get_total_price())
        request.session["campaign_id4"]=campaign.id
    except:
        pass
    messages.warning(request, "Product removed from your cart...")
    
    

    for key, value in request.session.items():
                print('{} => {}'.format(key, value))
    
    return redirect(url)
    #return redirect('cart:cart_detail')


def cart_detail(request):
    
    cart = Cart(request)
    #update burdan oluyor
    for item in cart:
        print(item)
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})

    coupon_apply_form = CouponApplyForm()

          
    return render(request, 'detail.html', {'cart': cart,'coupon_apply_form':coupon_apply_form,"update":'update'})
