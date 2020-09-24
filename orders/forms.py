from django import forms
from .models import Order
from localflavor.us.forms import USZipCodeField, USStateSelect, USStateField 
    
class OrderCreateForm(forms.ModelForm):
    postal_code = USZipCodeField()
    state = USStateSelect()
    class Meta:
        model = Order
        fields = [ 'address',
                  'postal_code', 'city','state',] #
        #widgets = {'order_total': forms.HiddenInput()}
