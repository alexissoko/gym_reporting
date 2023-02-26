from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reporting/sales', views.reporting_sales, name='reporting_sales'),
    path('reporting/payments', views.reporting_payments, name='reporting_payments'),
    path('reporting/activities', views.reporting_activities, name='reporting_activities'),
]  # end urlpatterns