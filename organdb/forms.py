from django import forms

class SearchForm(forms.Form):
    location = forms.CharField(label='Lokalizacja', max_length=70)
