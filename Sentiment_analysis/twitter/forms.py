from django import forms


class User(forms.Form):
    user = forms.CharField(label='', max_length = 20,  widget=forms.TextInput(attrs={'id': 'myModel'}))
