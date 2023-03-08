from django.forms import ModelForm

from . import models

class PaymentForm(ModelForm):
    class Meta:
        model = models.Payment
        fields = ['date', 'time', 'payment_type', 'user' , 'receiver', 'description', 'price', 'quota_number', 'units']
 