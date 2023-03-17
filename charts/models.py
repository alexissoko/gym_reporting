from django.db import models
from django import forms
from django.utils import timezone
import calendar
from datetime import datetime
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType



PAYMENT_CHOICES = (
   ('F', "efectivo"),
   ('T', 'transfer')
    )


MONTHLY_QUOTAS = {str(i):calendar.month_name[i] for i in range(13)}

SAFEBOX_CHOICES = (
   ('M', "Moni"),
   ('V', 'Vani'),
   ('B', "Board")
    )

EXPENSE_CHOICES = (
   ("TAX"),
   ('SERVICE'),
   ("PRODUCT")
    )

# Create your models here.
class Owner(models.Model):
    name = models.CharField(max_length=100, help_text=_('First and last name.'), verbose_name=_('name'))
    date = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name=_('date'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    # total = models.IntegerField(blank=True)

    def __str__(self) -> str:
        return self.name


# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    date = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name=_('date'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self) -> str:
        return self.name


# Create your models here.
class Activity(models.Model):
    class Meta:
        verbose_name = _('acitivity')
        verbose_name_plural = _('activities')
    name = models.CharField(max_length=100, verbose_name=_('name'))
    date = models.DateField(default=timezone.now, verbose_name=_('date'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    quota = models.IntegerField(blank=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self) -> str:
        return self.name


# Create your models here.
class Customer(models.Model):
    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        
    name = models.CharField(max_length=100, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('description'))
    date = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name=_('date'))
    
    def __str__(self) -> str:
        return  self.name


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    date = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name=_('date'))
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, blank=True, null=True
    )
    description = models.TextField(verbose_name=_('description'))
    status = models.BooleanField(verbose_name=_('active'), default=True)

    def __str__(self) -> str:
        return self.name


class Membership(models.Model):
    # invoice=models.ForeignKey(Input, on_delete=models.CASCADE)
    # seller=models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(default=timezone.now, verbose_name=_('date'))
    fee = models.BooleanField(verbose_name='Inscription')
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
   

    def __str__(self) -> str:
        return self.activity.name +'_'+ self.user.name.replace(' ','') + "_" + str(self.date)


class TypePayment(models.Model):

    # invoice=models.ForeignKey(Input, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100, null=True)
    # payment_type = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect())

    membership = models.ForeignKey(
        Membership, on_delete=models.CASCADE, blank=True, null=True
    )
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    membership.quantity = 1

    def __str__(self) -> str:
        return self.payment_type


class Payment(models.Model):
    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
    # invoice=models.ForeignKey(Input, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, verbose_name=_('date'))
    time = models.TimeField(default=datetime.now().strftime("%H:%M:%S"))
    payment_type = models.ForeignKey(TypePayment, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    receiver = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    price = models.IntegerField()
    units = models.IntegerField()
    
    # TODO: 12 quotas generator funcitonality
    quota_number = models.TextField(null=True, blank=True)#choices=MONTHLY_QUOTAS)

    def __str__(self) -> str:
        return self.user.name.replace(" ", "") + "_" + self.payment_type.membership.activity.name + "_" + str(self.date) + "_" + str(self.time)

class ExpenseType(models.Model):
    name = models.CharField(max_length=100, help_text=_('First and last name.'), verbose_name=_('name'))
    date = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name=_('date'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    # total = models.IntegerField(blank=True)

    def __str__(self) -> str:
        return self.name

class Expense(models.Model):
    class Meta:
        verbose_name = _('expense')
        verbose_name_plural = _('expense')
    name =models.TextField(verbose_name=_('name'))
    date = models.DateField(default=timezone.now, verbose_name=_('date'))
    price = models.IntegerField()
    expensetype = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))

    def __str__(self) -> str:
        return self.name +'_'+ _("Taxes") + "_" + str(self.date)
