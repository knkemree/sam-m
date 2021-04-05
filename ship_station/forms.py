from django import forms
from .models import File

class FileForm(forms.ModelForm):
    document = forms.FileField(required=True)
    class Meta:
        model = File
        fields = ('document',)

