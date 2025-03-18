from django.urls import path
from . import views

urlpatterns = [  
    path('login/', views.manager_login),
    path('dashboard/', views.view_dashboard_manager),
    path('approve-ticket/<int:ticket_id>', views.approve_ticket_manager),
    path('reject-ticket/<int:ticket_id>', views.reject_ticket),
    path('filter/', views.filter_dash),   
]