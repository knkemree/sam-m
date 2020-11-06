from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.template import loader
from django.shortcuts import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created, inform_admins
from cart.cart import Cart
from coupons.models import Campaign
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http.response import JsonResponse
from Delivery.forms import ShippingForm
from Delivery.models import Delivery_methods
#import weasyprint

import http.client
import mimetypes
import json
from django.core.mail import mail_admins

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

@login_required
def order_create(request):
    cart = Cart(request)
    
    shipping_form = ShippingForm()
    if request.method == 'POST':
        
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            
            order = form.save(commit=False)
            order.email = request.user
            order.first_name =request.user.first_name
            order.last_name =request.user.last_name
            order.order_profit = cart.get_total_price_after_discount() - cart.get_total_cost()
            order.campaign_id = request.session.get("campaign_id4")
            order.discounted_amount = cart.get_discount()
            order.campaign_discount = Campaign.objects.get(pk=request.session.get("campaign_id4")).campaign_discount
            try:
                order.delivery_method = Delivery_methods.objects.get(pk=request.session.get("delivery_id"))
                order.delivery_fees = order.delivery_method.fee
                    
            except Delivery_methods.DoesNotExist:
                order.delivery_method=None
                order.delivery_fees=0
            
            order.order_total = cart.get_total_price_after_discount()+order.delivery_fees

            pm = ((cart.get_total_price_after_discount() - cart.get_total_cost()) / cart.get_total_price_after_discount())*100
            decimal_pm = "%"+str(round(pm,2))
            order.profit_margin = decimal_pm
            order.company_name = request.user.company_name
            
            order = form.save(commit=False)

            order.save()
            for item in cart:
                print("order create itemin ici")
                print(item)
            
            for item in cart:
                OrderItem.objects.create(
                                        order=order,
                                        product=item['product'].product,
                                        variant = item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'],
                                        cost=item['cost'],
                                        )
            
                conn = http.client.HTTPSConnection("ecomdash.azure-api.net")
                payload = ''
                headers = {
                'Ocp-Apim-Subscription-Key': 'ce0057d8843342c8b3bb5e8feb0664ac',
                'ecd-subscription-key': '0e26a6d3e46145d5b7dd00a9f0e23c39'
                }
                conn.request("GET", "/api/Inventory?Type=Product&Id="+str(int(float(item['product'].ecomdashid))), payload, headers)
                res = conn.getresponse()
                data = res.read()
                veri = json.loads(data.decode("utf-8"))
                quantity_on_hand = veri["QuantityOnHand"]
                new_stock = int(quantity_on_hand) - int(item["quantity"])

                try:
                    conn = http.client.HTTPSConnection("ecomdash.azure-api.net")
                    payload1 = [{'Sku': str(item['product'].sku), 'Quantity': new_stock, 'WarehouseId': 2019007911.0}]
                    payload = str(payload1)
                    headers = {
                    'Ocp-Apim-Subscription-Key': 'ce0057d8843342c8b3bb5e8feb0664ac',
                    'ecd-subscription-key': '0e26a6d3e46145d5b7dd00a9f0e23c39',
                    'Content-Type': 'application/json'
                    }
                    conn.request("POST", "/api/inventory/updateQuantityOnHand", payload, headers)
                    res = conn.getresponse()
                    data = res.read()
                    print(data.decode("utf-8"))
                except:
                    pass


            # try:
            #     for i in Campaign.objects.filter(active=1):
            #         if i.amount_from < cart.get_total_price() <i.amount_to:
            #                 print("orders views sayfasi campaign iems")
            #                 print(i.id, i.campaign_discount, i.campaign_name)
                        
            #                 Order.objects.filter(id=order.id).update(campaign_id=i.id, campaign_discount=i.campaign_discount)
                            
            # except Campaign.DoesNotExist:
            #     request.session["campaign_id4"] = None
                

            cart.clear()
            try:
                del request.session["delivery_id"]
            except:
                pass
            
            
            # launch asynchronous task
            #order_created.delay(order.id, html_message_for_customer)
            #inform_admins.delay(order.id, html_message_for_admins)
            #order_created(order.id, html_message_for_customer)
            #inform_admins(order.id, html_message_for_admins)
            #mail_admins(subject="Test Email", message="Testing celery, rabbitMq and supervisor on production", fail_silently=False, connection=None, html_message=None)
            #add.delay(4, 5)
            # set the order in the session
            
            request.session['order_id'] = order.id
            
            # redirect for payment
            return redirect(reverse('payment:process'))

            
    else:
        form = OrderCreateForm()
    return render(request,
                  'create.html',
                  {'cart': cart, 'form': form,'shipping_form':shipping_form})


