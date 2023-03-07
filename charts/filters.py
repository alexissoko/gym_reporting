from django.forms import ModelForm
import django_filters
from . import models
from django_filters import CharFilter

class PaymentFilter(django_filters.FilterSet):
    id = CharFilter(field_name="id", lookup_expr="icontains")
    
    class Meta:
        model = models.Payment
        fields = ['user']
 