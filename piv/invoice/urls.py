from django.urls import path

from invoice import views

urlpatterns = [
  path("invoice", views.index, name="index"),
 ]