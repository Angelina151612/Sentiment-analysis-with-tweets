from django.forms import ModelForm

from .models import Usernames


class User(ModelForm):
    class Meta:
        model = Usernames
        fields = ["username"]
