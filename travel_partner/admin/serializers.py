from rest_framework import serializers
from travel_app.models import Manager, Employee, Admin, TicketDetails



class TicketDetail_for_admin(serializers.ModelSerializer):
    class Meta:
        model = TicketDetails
        fields = ['employee_id', 'manager_id', 'from_location', 'to_location', 'start_date', 'end_date', 'purpose_of_travel', 'manager_ticket_status', 'additional_request_admin']

class manager_list_serializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['username', 'id']

class Employee_list_serializer(serializers.ModelSerializer):    
    manager_id = serializers.CharField(source='manager.id', read_only=True)
    class Meta:
        model = Employee
        fields = ['username', 'id', 'manager_id']