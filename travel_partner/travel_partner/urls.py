
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('travel_app/', include('travel_app.urls')),
    path('admin/', include('admin.urls')),
    path('manager/', include('manager.urls')),
    path('employee/', include('employee.urls')),
]
