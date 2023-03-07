from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as logouts
from .models import *
from django.core import serializers
from .forms import *

# import pandas as pd
# from rest_framework.views import APIView
# from rest_framework.response import Response
import json
from .forms import PaymentForm


from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from slick_reporting.views import (
    SlickReportViewBase,
    SlickReportView as OriginalReportView,
)
from slick_reporting.fields import SlickReportField, Sum

# from chartjs.views.lines import BaseLineChartView
# from chartjs.views.lines import BaseLineChartView


def home(request):
    return render(request, "welcome.html")


@login_required
def reporting_sales(request):
    if request.GET.get("begin"):
        mesh_from = request.GET.get("begin")
    else:
        # TODO: default current year fix here
        mesh_from = "2000-01-01"
    if request.GET.get("until"):
        mesh_to = request.GET.get("until")
    else:
        mesh_to = timezone.now().strftime("%Y-%m-%d")
    payments = Payment.objects.filter(date__range=[mesh_from, mesh_to]).order_by(
        "-date"
    )
    # raw_data = serializers.serialize("json", Payment.objects.all())
    # test_data = payments.values("receiver","date", "price")

    receivers = {pay.receiver.name: {} for pay in payments}
    df_labels = sorted(
        [x[0].strftime("%Y-%m-%d") for x in payments.values_list("date").distinct()]
    )

    for landmark in df_labels:
        for name in receivers:
            if landmark not in receivers[name]:
                receivers[name][landmark] = 0

    for pay in payments:
        receivers[pay.receiver.name][pay.date.strftime("%Y-%m-%d")] += pay.price

    mydict = {
        "receivers": receivers,
        "df_labels": df_labels,
        "labels": list(receivers.keys()),
        "values": list(receivers.values()),
    }

    return render(request, "sales.html", context=mydict)


@login_required
def reporting_payments(request):
    json_data = serializers.serialize("json", Payment.objects.all())
    json_data2 = "[{" + json_data[39:]
    raw_data = Payment.objects.values()
    labels = list(raw_data.values()[0].keys())
    labels_1 = labels[1:]
    # breakpoint()

    mydict = {
        "json_data": json_data,
        "labels": labels
        }
    return render(request, "payments.html", context=mydict)


@login_required
def reporting_activities(request):
    if request.GET.get("begin"):
        mesh_from = request.GET.get("begin")
    else:
        # TODO: default current year fix here
        mesh_from = "2000-01-01"
    if request.GET.get("until"):
        mesh_to = request.GET.get("until")
    else:
        mesh_to = timezone.now().strftime("%Y-%m-%d")
    payments = Activity.objects.filter(date__range=[mesh_from, mesh_to]).order_by(
        "-date"
    )
    raw_data = serializers.serialize("json", Activity.objects.all())

    mydict = {
        "raw_data": raw_data,
    }
    # breakpoint()
    return render(request, "payments.html", context=mydict)


@login_required
def reporting_providers(request):
    print("boxes")
    if request.method == "POST":
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
        mesh_to = timezone.now().strftime("%Y-%m-%d")
    purchases = Membership.objects.filter(date__range=[mesh_from, mesh_to]).order_by(
        "-date"
    )

    bought_objs = {}
    for buy in purchases:
        if buy.invoice.name not in bought_objs:
            bought_objs[buy.invoice.name] = buy.invoice.id

    all_data = {prod.invoice.name: {} for prod in purchases}
    df_labels = sorted(
        [x[0].strftime("%Y-%m-%d") for x in purchases.values_list("date").distinct()]
    )

    mydict = {
        "owner": Owner.objects.all(),
        "bought_objs": bought_objs,
        "df_labels": df_labels,
        "labels": list(all_data.keys()),
        "values": list(all_data.values()),
    }
    return render(request, "providers.html", context=mydict)


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

    date_field = "date"
    # a date/datetime field on the report model

    # fields on the report model ... surprise !
    columns = ["date", "payment_type", "user", "receiver", "description", "price"]


class ActivitiesCrossTab(OriginalReportView):

    report_model = Activity
    date_field = "date"
    # group_by = 'sport'
    columns = ["date", "name", "description", "quota", "sport"]
    redirect_field_name = "control"

    # a date/datetime field on the report model

    # To activate Crosstab
    # crosstab_model = 'sport'
    # we corsstab on a foreignkey field

    # crosstab_columns = [SlickReportField.create(Sum, 'quota', name='quota__sum', verbose_name='Quota')
    # To be computed for each chosen entity in the crosstab.
    # ]


class GroupByViewSport(OriginalReportView):
    """
    We can have multiple charts, and multiple Calculation fields
    """

    report_model = Activity
    date_field = "date"
    group_by = "name"
    columns = [
        "name",
        SlickReportField.create(
            Sum, "quota", name="quota__sum", verbose_name="quota total"
        ),
        # SlickReportField.create(Sum, 'value', name='value__sum', verbose_name=_('Value $')),
        "description",
        "sport",
        "date",
    ]

    chart_settings = [
        {
            "type": "pie",
            "engine_name": "highcharts",
            "data_source": ["quota__sum"],
            "title_source": ["name"],
            "title": "Pie Chart (Quantities) Highcharts",
        },
        {
            "type": "pie",
            "engine_name": "chartsjs",
            "data_source": ["quota__sum"],
            "title_source": ["name"],
            "title": "Pie Chart (Quantities) ChartsJs",
        },
        {
            "type": "bar",
            "engine_name": "highcharts",
            "data_source": ["quota__sum"],
            "title_source": ["name"],
            "title": "Column Chart (Values)",
        },
        {
            "type": "bar",
            "engine_name": "chartsjs",
            "data_source": ["quota__sum"],
            "title_source": ["name"],
            "title": "Column Chart (Values)",
        },
    ]


def post_new(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.author = request.user
            payment.published_date = timezone.now()
            payment.save()
            return redirect("post_new", pk=payment.pk)
    else:
        form = PaymentForm()
    return render(request, "post_new.html", {"form": form})


def reporting_invoice(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    # form = PaymentForm(request.GET, instance=payment)
    payment.price
    return render(request, "post_invoice.html", {"payment": payment})


from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg
