from django.contrib import admin
from.models import *


# Register your models here.
admin.site.register(Owner)
admin.site.register(Sport)
admin.site.register(ClassSport)
admin.site.register(Customer)
admin.site.register(User)
admin.site.register(Membership)
admin.site.register(Payment)
admin.site.site_header = 'Pedidos'