from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    document = forms.FileField(required=False)
    class Meta:
        model = Document
        fields = ('document', )

