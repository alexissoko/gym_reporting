from django.db import models

# Create your models here.
class Owner(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    # total = models.IntegerField(blank=True)

    def __str__(self) -> str:
        return self.name


# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


# Create your models here.
class Activity(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    quota = models.IntegerField(blank=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.name


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, blank=True, null=True
    )
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Membership(models.Model):
    # invoice=models.ForeignKey(Input, on_delete=models.CASCADE)
    # seller=models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    fee = models.BooleanField(verbose_name='Inscripcion paga')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField()
    price = models.ForeignKey(Activity.price, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.invoice.name


class Payment(models.Model):
    # invoice=models.ForeignKey(Input, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    receiver = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)
    memebership = models.ForeignKey(
        Membership, on_delete=models.CASCADE, blank=True, null=True
    )
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.user.name + self.user.customername + self.memebership.activity.name


# Create your models here.
