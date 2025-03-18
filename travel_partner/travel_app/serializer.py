from rest_framework import serializers
from .models import Manager, Employee, Admin, TicketDetails

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class TicketDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketDetails
        fields = '__all__'

class TicketDetail_for_employee(serializers.ModelSerializer):
    manager_username = serializers.CharField(source='manager.username', read_only=True)
    employee_username = serializers.CharField(source='employee.username', read_only=True)

    class Meta:
        model = TicketDetails
        fields = [
            'employee_id', 'manager_id', 'from_location', 'to_location',
            'start_date', 'end_date', 'purpose_of_travel', 'manager_ticket_status',
            'manager_username', 'employee_username'
        ]

class TicketDetail_for_manager(serializers.ModelSerializer):
    class Meta:
        model = TicketDetails
        fields = ['employee_id', 'manager_id', 'from_location', 'to_location', 'start_date', 'end_date', 'purpose_of_travel', 'manager_ticket_status', 'additional_request_admin']

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