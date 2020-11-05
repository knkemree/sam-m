from django import forms



class updateQtyForm(forms.Form):
  file = forms.FileField()                

class SearchForm(forms.Form):
    query = forms.CharField()