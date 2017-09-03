from django import forms
from django.forms import ValidationError
from .models import DeliveryAddress


class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        # fields = "__all__"
        exclude = ['user','created','updated']
        fields = ['receiver','phoneNumber','zip','province','city','town','address','is_default']

    def clean_town(self):
        town = self.cleaned_data.get('town')
        if town == '':
            raise ValidationError('区域不能为空！')
        return town