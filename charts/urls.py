from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reporting/sales', views.reporting_sales, name='reporting_sales'),
    path('reporting/providers', views.reporting_providers, name='reporting_providers'),
]  # end urlpatterns