from django import forms
from cart.cart import Cart
from coupons.models import Campaign


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 31)]
class CartAddProductForm(forms.Form):
    
    quantity = forms.IntegerField(label='', widget=forms.TextInput(attrs={}))
    #quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int,#widget=forms.Select(attrs={'onchange':'this.form.submit();'}),)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput
                                  )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs.update({'class': 'special'})
        self.fields['quantity'].widget.attrs.update(value='1',min='1')


