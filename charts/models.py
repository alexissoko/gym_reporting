from django.db import models

# Create your models here.
class Owner(models.Model):
    name=models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    total=models.IntegerField(blank=True)
    
    def __str__(self) -> str:
        return self.name

# Create your models here.
class Sport(models.Model):
    name=models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    price=models.IntegerField(blank=True)
    owner=models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name

# Create your models here.
class ClassSport(models.Model):
    name=models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    quota=models.IntegerField(blank=True)
    # price=models.ForeignKey(Caja, on_delete=models.CASCADE, blank=True, null=True)
    sport=models.ForeignKey(Sport, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
    
# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    description=models.TextField()
    
    def __str__(self) -> str:
        return self.name
    
# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=100)
    date=models.DateField(null=True, blank=True)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    description=models.TextField()
    
    def __str__(self) -> str:
        return self.name
# Create your models here.
# class Sale(models.Model):
#     invoice=models.ForeignKey(Product, on_delete=models.CASCADE)
#     buyer=models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
#     date=models.DateField(null=True, blank=True)
#     description=models.TextField(null=True, blank=True)
#     payment=models.CharField(max_length=100, null=True, blank=True)
#     quantity = models.IntegerField()
#     price = models.IntegerField()
#     
#     
#     def __str__(self) -> str:
#         return self.invoice.name

class Payment(models.Model):
    #invoice=models.ForeignKey(Input, on_delete=models.CASCADE)
    payment_type=models.CharField(max_length=100)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # memebership=models.ForeignKey(Membership, on_delete=models.CASCADE, blank=True, null=True)

class Membership(models.Model):
    # invoice=models.ForeignKey(Input, on_delete=models.CASCADE)
    # seller=models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True, null=True)
    date=models.DateField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    payment=models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    
    def __str__(self) -> str:
        return self.invoice.name
# Create your models here.
