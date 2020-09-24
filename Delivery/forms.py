from django import forms
from Delivery.models import Delivery_methods


class ShippingForm(forms.ModelForm):
    
        
    choices = Delivery_methods.objects.all()
    delivery_method = forms.ModelChoiceField(
                                queryset=choices, 
                                required=False, 
                                widget=forms.Select(attrs={'onchange':'changeSelectedvalue(); this.form.submit();',}),
                                #empty_label'i degistirirsen create.html'de de degistirmen gerekenler var.
                                #empty_label'in stirng'i ile bos oldugunda alert vermek icin yazdigin kodun string'i ayni olmasi lazim.
                                empty_label="----Select----", 
                                
                                )
    #initial = {'delivery_method': Delivery_methods.objects.all().first() }


    class Meta:
        model = Delivery_methods
        fields = ["delivery_method"]

    def clean_delivery_method(self):
        delivery_method = self.cleaned_data.get("delivery_method")
        
        #eger delivery_method ----Select---- olarak secilirse form valid olmayacak
        if delivery_method == None:
    
            raise forms.ValidationError("Delivery method cannot be left blank.")
        
        return delivery_method
    
    