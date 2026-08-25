from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseNotFound

from invoice.models import Invoice


@login_required(login_url='login')
def invoice_view(request):
    """
    Show invoices
    :param request:
    :return:
    """
    invoices = Invoice.objects.all().order_by("-issue_date")
    return render(request, "invoice/invoices.html", {"invoices": invoices })


@login_required(login_url='login')
def invoice_create_view(request):
    """if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            messages.success(request, f"Company '{company.name}' created successfully.")
            return redirect("companies")
    else:
        form = CompanyForm()
    return render(request, "crm/company_form.html", {"form": form, "mode": "Create"})
"""
    return HttpResponseNotFound("Not implemented")


@login_required(login_url='login')
def invoice_edit_view(request, pk):
    return HttpResponseNotFound("Not implemented")


@login_required(login_url='login')
def invoice_delete_view(request, pk):
    return HttpResponseNotFound("Not implemented")