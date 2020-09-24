from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET
from .models import Coupon, Campaign
from .forms import CouponApplyForm
from django.conf import settings
from cart.cart import Cart
from orders.models import Order
from django.http.response import HttpResponse, JsonResponse
import json
from django.views.generic import View

@require_POST
def coupon_apply(request):
    cart = Cart(request)
        
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        try:
            campaign = Campaign.objects.get(active=1, amount_from__lte=cart.get_total_price(),amount_to__gte=cart.get_total_price())
            form.campaign_id = campaign.id
            form.campaign_discount =campaign.campaign_discount
            form.campaign_name =campaign.campaign_name
            #del request.session['campaign_id']
            request.session['campaign_id'] = campaign.id
            request.session.modified = True
            request.session.save()
            
        except Campaign.DoesNotExist:
            pass
            request.session['campaign_id'] = None
    
    return redirect('cart:cart_detail')


def campaign_apply(request):
    cart = Cart(request)
    print("calisiyormu")
    if request.method == 'POST':
        total_price = request.POST.get("campaign_discount") 
        print("ajaxtan total price'i aldi mi kontrol ediyirum")
        print(total_price)
        try:
            campaign = Campaign.objects.get(active=1, amount_from__lte=cart.get_total_price(),amount_to__gte=cart.get_total_price())
            request.session['campaign_id2'] = campaign.id
            request.session.modified = True
            request.session.save()
            print(campaign.id)
            for key, value in request.session.items():
                print('{} => {}'.format(key, value))
                print("ajax deneme oluyor")
            
            
        except Campaign.DoesNotExist:
            request.session['campaign_id2'] = None
            
            
        #return redirect('cart:cart_detail')
        return JsonResponse({"success":True}, status=200)
    else:
        print("ajax deneme olmuyor")
    return JsonResponse({"success":False}, status=400)