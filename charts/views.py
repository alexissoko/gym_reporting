from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as logouts
from .models import *
from .filters import *
from django.core import serializers
from django.http import JsonResponse
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

    receivers = {pay.receiver.name: {}  for pay in payments}
    totals = {pay.receiver.name: 0  for pay in payments}
    sports_slices = {pay.user.activity.sport.name: {}  for pay in payments}
    totals_sport = {pay.user.activity.sport.name: 0  for pay in payments}
    df_labels = sorted(
        [x[0].strftime("%Y-%m-%d") for x in payments.values_list("date").distinct()]
    )

    for landmark in df_labels:
        for name in receivers:
            if landmark not in receivers[name]:
                receivers[name][landmark] = 0

    for pay in payments:
        receivers[pay.receiver.name][pay.date.strftime("%Y-%m-%d")] += pay.price
        totals[pay.receiver.name] += pay.price
        totals_sport[pay.user.activity.sport.name] += pay.price
    
    final_totals = [{"owner":k, "total":v} for k,v in totals.items()]
    totals_sport = [{"sport":k, "total":v} for k,v in totals_sport.items()]
 
    mydict = {
        "receivers": receivers,
        "totals": totals,
        "df_labels": df_labels,
        "final_totals": final_totals,
        "sports_slices": sports_slices,
        "totals_sport": totals_sport 

    }
    # breakpoint()
    return render(request, "sales.html", context=mydict)

@login_required
def reporting_expenses(request):
    if request.GET.get("begin"):
        mesh_from = request.GET.get("begin")
    else:
        # TODO: default current year fix here
        mesh_from = "2000-01-01"
    if request.GET.get("until"):
        mesh_to = request.GET.get("until")
    else:
        mesh_to = timezone.now().strftime("%Y-%m-%d")
    payments = Expense.objects.filter(date__range=[mesh_from, mesh_to]).order_by(
        "-date"
    )

    receivers = {pay.expensetype.name: {}  for pay in payments}
    totals = {pay.expensetype.name: 0  for pay in payments}
    sports_slices = {pay.owner.name: {}  for pay in payments}
    totals_sport = {pay.owner.name: 0  for pay in payments}
    df_labels = sorted(
        [x[0].strftime("%Y-%m-%d") for x in payments.values_list("date").distinct()]
    )

    for landmark in df_labels:
        for name in receivers:
            if landmark not in receivers[name]:
                receivers[name][landmark] = 0

    for pay in payments:
        receivers[pay.expensetype.name][pay.date.strftime("%Y-%m-%d")] += pay.price
        totals[pay.expensetype.name] += pay.price
        totals_sport[pay.owner.name] += pay.price
    
    final_totals = [{"owner":k, "total":v} for k,v in totals.items()]
    totals_sport = [{"sport":k, "total":v} for k,v in totals_sport.items()]
 
    mydict = {
        "receivers": receivers,
        "totals": totals,
        "df_labels": df_labels,
        "final_totals": final_totals,
        "sports_slices": sports_slices,
        "totals_sport": totals_sport 

    }
    # breakpoint()
    return render(request, "expenses.html", context=mydict)


@login_required
def reporting_payments(request):
    json_data = serializers.serialize("json", Payment.objects.all())
    json_data2 = "[{" + json_data[39:]
    raw_data = Payment.objects.values()

    labels = ["model"] + list(raw_data.values()[0].keys())
    labels_1 = labels[1:]
    raw_data = JsonResponse(list(Payment.objects.values()),safe = False)

    mydict = {
        "json_data": json_data,
        "raw_data": raw_data,
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


def post_new(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.author = request.user
            payment.published_date = timezone.now()
            payment.save()
            return redirect("reporting_invoice", pk=payment.pk)
    else:
        form = PaymentForm()
        return render(request, "post_new.html", {"form": form})


def reporting_invoice(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, "post_invoice.html", {"payment": payment})


def payment_search(request, pk=None):
    if request.method == "POST":
        payment = get_object_or_404(Payment, pk=pk)
        return render(request, "post_invoice.html", {"payment": payment})
    else:
        payments = Payment.objects.all()
        myFilter = PaymentFilter(request.GET, queryset=payments)
        payments = myFilter.qs
        context = {
            'myFilter': myFilter,
            'payments': payments,
        }
        return render(request, 'payment_search.html', context)
