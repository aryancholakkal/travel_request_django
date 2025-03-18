from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.employee_login),
    path('tickets/', views.manage_employee_tickets),
    path('tickets/<int:ticket_id>/', views.manage_employee_tickets,),
    path('filter_dash', views.filter_dash, ),
]