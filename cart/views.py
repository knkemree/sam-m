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
def choose_size(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=product_id)
    print("product nedir")
    print(product)
    if request.method == "POST":
        for item in request.POST:
            key = item
            val = request.POST[key]
            print("variant val and key")
            print(val, key)
            if val == "-----":
                try:
                    del request.session["variation_id"]
                except:
                    pass
            else:
                try:
                    variation = Variation.objects.get(product=product, category__iexact=key, title__iexact=val)
                    print("selected variation id")
                    request.session["variation_id"] = variation.id
                    print(request.session.get("variation_id"))
                    messages.success(request, "Choosed size")
                except:
                    pass

    # else:
    #     try:
    #         del request.session["variation_id"]
    #     except:
    #         pass

    return HttpResponseRedirect(url)
    #return redirect('cart:cart_detail')

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
           product = get_object_or_404(Variation, id=request.session.get("variation_id"))  #bunu cart detail sayfasini guncellerken kullaniyor
        
        cart.add(
                 product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])

        if cd['override'] == True:
            messages.success(request, "Cart updated...")
        else:
            messages.success(request, "Added to cart...")

    else:
        del request.session["variation_id"]
    
    try:
        campaign = Campaign.objects.get(active=1, amount_from__lte=cart.get_total_price(),amount_to__gte=cart.get_total_price())
        request.session["campaign_id4"]=campaign.id
    except: 
        pass

    # for key, value in request.session.items():
    #             print('{} => {}'.format(key, value))

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
