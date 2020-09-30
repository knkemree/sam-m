from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from coupons.models import Campaign
from Delivery.models import Delivery_methods
from django.http import HttpResponseRedirect
from django.contrib import messages



@require_POST
def cart_add(request, product_id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    for key, value in request.session.items():
                print('{} => {}'.format(key, value))
                
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        messages.success(request, "Product added to cart...")
    
    campaign = Campaign.objects.get(active=1, amount_from__lte=cart.get_total_price(),amount_to__gte=cart.get_total_price())
    request.session["campaign_id4"]=campaign.id
    


    print("cart add yapinca campaign id print oluyor mu")
    print(campaign.id)
    
    return HttpResponseRedirect(url)
    #return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    campaign = Campaign.objects.get(active=1, amount_from__lte=cart.get_total_price(),amount_to__gte=cart.get_total_price())
    
    request.session["campaign_id4"]=campaign.id
    
    return redirect(url)
    #return redirect('cart:cart_detail')


def cart_detail(request):
    
    cart = Cart(request)

    #update burdan oluyor
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})

    coupon_apply_form = CouponApplyForm()
    
          
    return render(request, 'detail.html', {'cart': cart,'coupon_apply_form':coupon_apply_form})
