from rest_framework import serializers
from travel_app.models import Manager, Employee, Admin, TicketDetails

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
