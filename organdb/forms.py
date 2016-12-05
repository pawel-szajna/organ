from django import forms

class SearchForm(forms.Form):
    ACTION_CHOICES = [
        ('b', 'obojętna'),
        ('mechaniczna', 'mechaniczna'),
        ('pneumatyczna', 'pneumatyczna'),
        ('elektro-pneumatyczna', 'elektro-pneumatyczna'),
        ('elektryczna', 'elektryczna'),
    ]

    city = forms.CharField(label='Miejscowość', min_length=3, max_length=30, required=False)
    location = forms.CharField(label='Lokalizacja', min_length=3, max_length=70, required=False)
    keyboards = forms.IntegerField(label='Klawiatury', min_value=1, max_value=9, required=False)
    pedalboard = forms.ChoiceField(label='Pedał', choices=(('b', 'obojętnie'), ('y', 'tak'), ('n', 'nie')),
                                   widget=forms.RadioSelect, required=False)
    stops_min = forms.IntegerField(label='Minimalna liczba głosów', min_value=1, required=False)
    stops_max = forms.IntegerField(label='Maksymalna liczba głosów', min_value=1, required=False)
    key_action = forms.ChoiceField(label='Traktura gry', choices=ACTION_CHOICES, required=False)
    stop_action = forms.ChoiceField(label='Traktura rejestrów', choices=ACTION_CHOICES, required=False)