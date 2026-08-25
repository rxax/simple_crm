from django.urls import path

from invoice import views

urlpatterns = [
  path("", views.invoice_view, name="invoices"),
    path("new/", views.invoice_create_view, name="invoice_create"),
    path("<int:pk>/edit/", views.invoice_edit_view, name="invoice_edit"),
    path("<int:pk>/delete/", views.invoice_delete_view, name="invoice_delete"),
 ]