from django.urls import path
from . import views

urlpatterns = [
     

    path('logout/', views.user_logout),
    path('request_edit/', views.request_edit,),
    path('search_records/', views.search_records,), 
    path('sort_requests/', views.sort_requests,),
    path('search_by_person/', views.search_by_person,),
    path('process_approved_request/', views.process_approved_request,),
]