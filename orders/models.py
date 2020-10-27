from django.db import models
from products.models import Product, Variation
from account.models import Customers
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon, Campaign
from Delivery.models import Delivery_methods
from django.urls import reverse
#from localflavor.us.forms import USStateSelect

class Order(models.Model):
    company_name =models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.ForeignKey(Customers, on_delete=models.CASCADE, blank=True, related_name="orders")
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment = models.BooleanField(default=False)
    fulfillment = models.BooleanField(default=False)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit_margin = models.CharField(max_length=50, blank=True, null=True)
    braintree_id = models.CharField(max_length=150, blank=True)
                                    
    campaign = models.ForeignKey(Campaign,
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    campaign_discount = models.IntegerField(default=0, help_text="Discount by percentage. Maximum 100.",
                                  validators=[MinValueValidator(0),
                                      MaxValueValidator(100)])
    #discounted_amount = models.IntegerField(default=0)
    discounted_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    delivery_method = models.ForeignKey(Delivery_methods, on_delete=models.CASCADE, blank=True, null=True)
    delivery_fees = models.IntegerField(default=0)
    

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f'Order {self.id}'

    def delivery_fee(self):
        print(self.delivery_fees )
        return self.delivery_fees 

    def get_total_cost(self):
        total_cost = sum(item.get_customer_cost() for item in self.items.all())
        return total_cost - total_cost * \
            (self.campaign_discount / Decimal(100))+self.delivery_fees 

    def cart_total(self):
        total_cost = sum(item.get_customer_cost() for item in self.items.all())
        return total_cost

    def get_absolute_url(self):
        return reverse('order_details',
                       args=[self.id])

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE,
                              )
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    variant = models.CharField(max_length=50)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kw):
        old = type(self).objects.get(pk=self.pk) if self.pk else None
        super(OrderItem, self).save(*args, **kw)

        if old and old.price != self.price: # Field has changed
            print("BURDA BISEYLER YAPMAM LAZIM")
            a = OrderItem.objects.filter(order_id=self.order_id)
            sumof_order_total = 0
            sumof_order_cost = 0
            sumof_order_profit = 0
            for i in a:
                sumof_order_total = sumof_order_total + (i.price * i.quantity)
                sumof_order_cost = sumof_order_cost + (i.cost * i.quantity)
                sumof_profit_margin = "%"+str(round(((sumof_order_total - sumof_order_cost)/sumof_order_total)*100,2))
                sumof_order_profit = sumof_order_total - sumof_order_cost

            b = Order.objects.get(id=self.order_id)
            b.order_total = sumof_order_total
            b.profit_margin = sumof_profit_margin
            b.order_profit = sumof_order_profit
            b.save()

        if old and old.quantity != self.quantity: # Field has changed
            a = OrderItem.objects.filter(order_id=self.order_id)
            sumof_order_total = 0
            sumof_order_cost = 0
            sumof_order_profit = 0
            for i in a:
                
                sumof_order_total = sumof_order_total + (i.price * i.quantity)
                sumof_order_cost = sumof_order_cost + (i.cost * i.quantity)
                sumof_profit_margin = "%"+str(round(((sumof_order_total - sumof_order_cost)/sumof_order_total)*100,2))
                sumof_order_profit = sumof_order_total - sumof_order_cost
            b = Order.objects.get(id=self.order_id)
            b.order_total = sumof_order_total
            b.profit_margin = sumof_profit_margin
            b.order_profit = sumof_order_profit
            b.save()
            
        if old and old.cost != self.cost:
            a = OrderItem.objects.filter(order_id=self.order_id)
            sumof_order_total = 0
            sumof_order_cost = 0
            sumof_order_profit = 0
            
            for i in a:
                sumof_order_total = sumof_order_total + (i.price * i.quantity)
                sumof_order_cost = sumof_order_cost + (i.cost * i.quantity)
                sumof_profit_margin = "%"+str(round(((sumof_order_total - sumof_order_cost)/sumof_order_total)*100,2))
                sumof_order_profit = sumof_order_total - sumof_order_cost
            
            b = Order.objects.get(id=self.order_id)
            b.order_profit = sumof_order_profit
            b.profit_margin = sumof_profit_margin
            b.save()
    def __str__(self):
        return str(self.id)

    def get_customer_cost(self):
        return self.price * self.quantity

    def get_seller_cost(self):
        return self.cost * self.quantity

    
    