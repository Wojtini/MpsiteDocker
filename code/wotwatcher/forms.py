from django import forms

from wotwatcher.models import TankExpectations


class WN8Form(forms.Form):
    data = TankExpectations.objects.all()
    nick = forms.CharField(max_length=150)
    tank = forms.ModelChoiceField(queryset=data, required=True)
