from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("profile/", views.profile_view, name="profile"),
    path("companies/", views.company_list_view, name="companies"),
    path("companies/new/", views.company_create_view, name="company_create"),
    path("companies/<int:pk>/edit/", views.company_edit_view, name="company_edit"),
    path("companies/<int:pk>/delete/", views.company_delete_view, name="company_delete"),
    path("logout/", views.logout_view, name="logout"),
    path("active-company/", views.active_company_update, name="active_company"),
]