from django import forms
from cart.cart import Cart
from coupons.models import Campaign


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 31)]
class CartAddProductForm(forms.Form):
    
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int,
                                
                                #widget=forms.Select(attrs={'onchange':'this.form.submit();'}),
                                )
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput
                                  )



