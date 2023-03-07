from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reporting/sales', views.reporting_sales, name='reporting_sales'),
    path('reporting/payments', views.reporting_payments, name='reporting_payments'),
    path('reporting/<int:pk>/payments', views.reporting_invoice, name='reporting_invoice'),
    path('reporting/activities', views.reporting_activities, name='reporting_activities'),
    path('payment/search/', views.payment_search, name='payment_search'),
    path('post/new/', views.post_new, name='post_new'),
    # path('post/<int:pk>/edit/', views.post_detail, name='post_detail'),
]  # end urlpatterns