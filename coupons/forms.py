from django import forms

class CouponApplyForm(forms.Form):
    campaign_id = forms.CharField(required=False,widget=forms.HiddenInput,initial=False)
    campaign_discount = forms.CharField(required=False,widget=forms.HiddenInput)
    campaign_name = forms.CharField(required=False,widget=forms.HiddenInput)
    #campaign_name = forms.CharField(required=False,widget=forms.HiddenInput,initial=False)

