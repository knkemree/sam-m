from django import forms
from .models import File

class FileForm(forms.ModelForm):
    document = forms.FileField(required=True)
    class Meta:
        model = File
        fields = ('document',)


class GTINForm(forms.Form):
    gtin = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='GTIN')

    

