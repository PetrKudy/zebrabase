from django.forms import ModelForm
from django import forms
from management.models import Substock, Stock,Fishline


class DetailFishForm(forms.ModelForm):
        amount = forms.IntegerField()
        birthdate = forms.DateField()
        class Meta:
            model = Fishline
            fields = ['name','description']
