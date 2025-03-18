from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ("Active", "Active"),
    ("Inactive", "Inactive")
)

MANAGER_TICKET_CHOICES = (
    ("Approved", "Approved"),
    ("Request Edit", "Request Edit"),
    ("Rejected", "Rejected"),
    ("Not Responded", "Not Responded")
)

TRAVEL_MODE_CHOICES = (
    ("Bus", "Bus"), 
    ("Train", "Train"), 
    ("Plane", "Plane"),         
    ("Ship", "Ship"), 
)

ADMIN_MODE_CHOICES = (
    ("Open","Open"),
    ("Close","Close")
)

class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    user= models.OneToOneField(User,on_delete=models.SET_NULL, null=True)

class Manager(models.Model):
    username = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )
    user= models.OneToOneField(User,on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=100,null=True)

class Employee(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.PROTECT, related_name="employees")
    username = models.CharField(max_length=100, unique=True)
    date_of_joining = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )
    user= models.OneToOneField(User,on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=100,null=True)

class TicketDetails(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="tickets")
    manager = models.ForeignKey(Manager, on_delete=models.PROTECT, related_name="tickets")
    date_of_request = models.DateField()
    from_location = models.CharField(max_length=100) 
    to_location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    manager_ticket_status = models.CharField(
        max_length=20,
        choices=MANAGER_TICKET_CHOICES,
        default="Not Responded"  
    )
    admin_ticket_status = models.CharField(
        max_length=20,
        choices=ADMIN_MODE_CHOICES,
        default="Not Responded"  
    )
    preferred_travel_mode = models.CharField(
        max_length=10,
        choices=TRAVEL_MODE_CHOICES,
        default="Bus"
    )
    is_lodging_req = models.BooleanField(default=False)
    purpose_of_travel = models.CharField(max_length=100) 
    additional_note_employee = models.TextField(blank=True, null=True) 
    additional_request_admin = models.TextField(blank=True, null=True) 
    additional_request_manager = models.TextField(blank=True, null=True) 
    no_of_submission = models.PositiveIntegerField(default=1)

