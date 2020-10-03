from decimal import Decimal
from django.conf import settings
from products.models import Product, Variation
from coupons.models import Coupon, Campaign
from Delivery.models import Delivery_methods


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        #self.coupon_id = self.session.get('coupon_id')
        
        self.campaign_id = self.session.get('campaign_id4')
        self.delivery_id = self.session.get('delivery_id')
        self.variation_id = self.session.get('variation_id')
        
        
        

    def add(self, variation_id, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        variation_id daha once yoktu ben ekledim.
    

        """


        variation_price = Variation.objects.get(id=variation_id).price
        variation_cost = Variation.objects.get(id=variation_id).cost
        
        #varianttan once urun cost ve price'i product.price ve product.cost yazilarak aliniyordu.
        #product_id = str(product.id)
        product_id = str(variation_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(variation_price),
                                     'cost': str(variation_cost),
                                     }

        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        
        # get the product objects and add them to the cart
        products = Variation.objects.filter(id__in=product_ids)
        print("iter")
        print(products)
        cart = self.cart.copy()
        
        for product in products:
            print(product)
            cart[str(product.id)]['product'] = product
        
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['cost'] = Decimal(item['cost'])
            item['total_cost'] = item['cost'] * item['quantity'] 
            yield item
        

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()) #en bastaki decimal icerisideydi

    def get_single_item_total_price(self):
        
        prices = []
        for i in [Decimal(item['price']) * item['quantity'] for item in self.cart.values()]:
            prices.append(float(i))

        return prices

    def get_total_cost(self):
        return sum(Decimal(item['cost']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    

    @property
    def campaign(self):
        if self.campaign_id:
            try:
                return Campaign.objects.get(id=self.campaign_id)
            except Campaign.DoesNotExist:
                pass
        return None
    
    def get_discount(self):
        if self.campaign:
            return (self.campaign.campaign_discount / Decimal(100)) \
                * self.get_total_price()
        return Decimal(0)
    def get_total_price_after_discount(self):
        
        return self.get_total_price() - self.get_discount()

    @property
    def shipment(self):
        if self.delivery_id:
            try:
                return Delivery_methods.objects.get(id=self.delivery_id)
            except Delivery_methods.DoesNotExist:
                pass
        return None

    def shipment_fee(self):
        if self.delivery_id:
        # delivery'nin kac paradan sonra bedava olacagini burdan ayarliyoruz.
            if self.get_total_price_after_discount()>=500:
                shipment_fee = Decimal(0)
    
                return shipment_fee
            else:
                shipment_fee = Decimal(self.shipment.fee)
                
                return shipment_fee

    def get_total_price_after_discount_and_shipment_fee(self):
        #try except kontrolu koymazsam sag ustteki sepet totalini yapmiyor
        try:
            return self.get_total_price_after_discount() + self.shipment_fee()
        except:
        
            return self.get_total_price_after_discount()
        #return self.get_total_price_after_discount() + self.shipment.fee()