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




@require_POST
def cart_add(request, product_id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    

    if request.method == "POST":
        for item in request.POST:
            key = item
            val = request.POST[key]
            print("bos oldugunda val nedir")
            print(val)
            if val == "-----":
                try:
                    del request.session["variation_id"]
                except:
                    pass
            else:
                try:
                    variation = Variation.objects.get(product=product, category__iexact=key, title__iexact=val)
                    print("variation session numarasi bos olugunde nedir")

                    request.session["variation_id"] = variation.id
                    print(request.session.get("variation_id"))
                except:
                    pass

    
    

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
                 variation_id=request.session.get("variation_id"),
                 product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        messages.success(request, "Cart updated...")
    else:
        del request.session["variation_id"]
    

    
    campaign = Campaign.objects.get(active=1, amount_from__lte=cart.get_total_price(),amount_to__gte=cart.get_total_price())
    request.session["campaign_id4"]=campaign.id

    
    


    for key, value in request.session.items():
                print('{} => {}'.format(key, value))


    return HttpResponseRedirect(url)
    #return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart(request)
    product = get_object_or_404(Variation, id=product_id)
    cart.remove(product)
    campaign = Campaign.objects.get(active=1, amount_from__lte=cart.get_total_price(),amount_to__gte=cart.get_total_price())
    messages.warning(request, "Product deleted from your cart...")
    
    request.session["campaign_id4"]=campaign.id

    for key, value in request.session.items():
                print('{} => {}'.format(key, value))
    
    return redirect(url)
    #return redirect('cart:cart_detail')


def cart_detail(request):
    
    cart = Cart(request)
    print("cart_detail")
    print(cart)
    #update burdan oluyor
    for item in cart:
        print(item)
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})

    coupon_apply_form = CouponApplyForm()
        
          
    return render(request, 'detail.html', {'cart': cart,'coupon_apply_form':coupon_apply_form})
