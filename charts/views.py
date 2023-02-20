from django.shortcuts import render, redirect
from django.contrib.auth import logout as logouts
from .models import *
from .forms import *
# import pandas as pd
# from rest_framework.views import APIView
# from rest_framework.response import Response
import json

from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from slick_reporting.views import SlickReportViewBase, SlickReportView as OriginalReportView
from slick_reporting.fields import SlickReportField, Sum

# from chartjs.views.lines import BaseLineChartView
# from chartjs.views.lines import BaseLineChartView


def home(request):
    return render(request, 'welcome.html')

@login_required
def reporting_sales(request):
    if request.GET.get("begin"):
        mesh_from = request.GET.get("begin")
    else:
        mesh_from = "2000-01-01"
    if request.GET.get("until"):
        mesh_to = request.GET.get("until")
    else:
        mesh_to = timezone.now().strftime('%Y-%m-%d')
    sales = Owner.objects.filter(date__range=[mesh_from, mesh_to]).order_by("-date")
    
    sold_objs = {}
    for sale in sales:
        if sale.invoice.name not in sold_objs:
            sold_objs[sale.invoice.name] = sale.invoice.id
    
    all_data = {prod.invoice.name: {} for prod in sales}
    df_labels = sorted([x[0].strftime('%Y-%m-%d') for x in sales.values_list("date").distinct()])

    for sale in sales:
        all_data[sale.invoice.name][sale.date.strftime('%Y-%m-%d')] = sale.quantity
    
    for label in df_labels:
        for k, v in all_data.items():
            if label not in v:
                all_data[k][label] = 0
    
    for k,v in all_data.items():
        all_data[k] = [all_data[k][x] for x in sorted(all_data[k])]


    mydict= {
        'sold_objs':sold_objs,
        "df_labels" : df_labels,
        "labels" : list(all_data.keys()),
        "values" : list(all_data.values()),
    
    }
    return render(request, 'sales.html', context=mydict)

@login_required
def reporting_providers(request):
    print('boxes')
    if request.method == 'POST':
        pass
    else:
        print(request.GET.getlist("boxes"))
        
    if request.GET.get("begin"):
        mesh_from = request.GET.get("begin")
    else:
        mesh_from = "2000-01-01"
    if request.GET.get("until"):
        mesh_to = request.GET.get("until")
    else:
        mesh_to = timezone.now().strftime('%Y-%m-%d')
    purchases = Membership.objects.filter(date__range=[mesh_from, mesh_to]).order_by("-date")

    bought_objs = {}
    for buy in purchases:
        if buy.invoice.name not in bought_objs:
            bought_objs[buy.invoice.name] = buy.invoice.id
    
    all_data = {prod.invoice.name: {} for prod in purchases}
    df_labels = sorted([x[0].strftime('%Y-%m-%d') for x in purchases.values_list("date").distinct()])

    for sale in purchases:
        all_data[sale.invoice.name][sale.date.strftime('%Y-%m-%d')] = sale.quantity
    
    for label in df_labels:
        for k, v in all_data.items():
            if label not in v:
                all_data[k][label] = 0
    
    for k,v in all_data.items():
        all_data[k] = [all_data[k][x] for x in sorted(all_data[k])]


    mydict= {
        'owner': Owner.objects.all(),
        'bought_objs': bought_objs,
        "df_labels" : df_labels,
        "labels" : list(all_data.keys()),
        "values" : list(all_data.values()),
    
    }
    return render(request, 'providers.html', context=mydict)

class SimpleListReport(OriginalReportView):
    """
    Let's start by creating a page where we can filter our report_model record / dataset.
    Slick Reporting come with `SlickReportView` CBV.

    By adding this view to your urls.py
        path('', views.SimpleListReport.as_view()),
    You'll see a results page as the shown below
    """
    report_model = Payment
    # the model containing the data we want to analyze

    date_field = 'date'
    # a date/datetime field on the report model

    # fields on the report model ... surprise !
    columns = ['date', 'payment_type', 'user', 'receiver', 'description', 'price']

class GroupByViewActivity(OriginalReportView):
    """
    We can have multiple charts, and multiple Calculation fields
    """

    report_model = Sport
    date_field = 'date'
    group_by = 'owner'
    columns = ['name',
               SlickReportField.create(Sum, 'owner', name='owner__sum', verbose_name='owner total'),
               # SlickReportField.create(Sum, 'value', name='value__sum', verbose_name=_('Value $')),
               'description',
               ]

    chart_settings = [
        {'type': 'pie',
         'engine_name': 'highcharts',
         'data_source': ['owner__sum'],
         'title_source': ['name'],
         'title': 'Pie Chart (Quantities) Highcharts'
         },
        {'type': 'pie',
         'engine_name': 'chartsjs',
         'data_source': ['owner__sum'],
         'title_source': ['name'],
         'title': 'Pie Chart (Quantities) ChartsJs'
         },
        {'type': 'bar',
         'engine_name': 'highcharts',
         'data_source': ['owner__sum'],
         'title_source': ['name'],
         'title': 'Column Chart (Values)'
         },
        {'type': 'bar',
         'engine_name': 'chartsjs',
         'data_source': ['owner__sum'],
         'title_source': ['name'],
         'title': 'Column Chart (Values)'
         },
    ]