from django import forms
from .models import File

class FileForm(forms.ModelForm):
    document = forms.FileField(required=True)
    class Meta:
        model = File
        fields = ('document',)


class GTINForm(forms.Form):
    gtin = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'scan item GTIN or ATTN...','rows':1}), label='')

    

