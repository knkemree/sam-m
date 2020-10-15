import braintree
import stripe

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order

#from orders.tasks import order_created, inform_admins
stripe.api_key = "sk_test_LGKgGvfpnOtCepkfRQxOpFub"
STRIPE_PUB_KEY = 'pk_test_c6fSv46teTU4tycT1Aiv7ezy'


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    print("musterinin odedigi miktari gosteriyor dogru mu diye kontrol et")
    print(total_cost)
    print("order delivery fee")
    print(order.delivery_fee())

    if request.method == 'POST':
        print(request.POST)
        token = request.POST.get('stripeToken')
        print("token burda")
        print(token)
        result = stripe.Charge.create(
            amount=100,
            #amount=int(total_cost*100),
            currency="usd",
            source=token,
            #customer=request.user,
            description="My First Test Charge (created for API docs)",
        )
        print("result burda")
        print(result)

        if result.status == "succeeded":
            print("yeaaaaaah!!!!")
            # mark the order as paid
            
            order.payment = True
            # store the unique transaction id
            order.braintree_id = result.id
            order.save()
            # launch asynchronous task
            #order_created.delay(order.id, html_message_for_customer)
            #inform_admins.delay(order.id, html_message_for_admins)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        #client_token = gateway.client_token.generate()
        return render(request,
                      'process.html',
                      {'order': order,
                       'publish_key':STRIPE_PUB_KEY})

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
def payment_process1(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    print("musterinin odedigi miktari gosteriyor dogru mu diye kontrol et")
    print(total_cost)
    print("order delivery fee")
    print(order.delivery_fee())
    
    
    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            
            # mark the order as paid
            
            order.payment = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # launch asynchronous task
            #order_created.delay(order.id, html_message_for_customer)
            #inform_admins.delay(order.id, html_message_for_admins)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request,
                      'process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    return render(request, 'done.html')
def payment_canceled(request):
    return render(request, 'canceled.html')
