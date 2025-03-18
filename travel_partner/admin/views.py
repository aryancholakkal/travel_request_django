import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.permissions import AllowAny
from travel_app.models import TicketDetails, Manager, Employee
from .serializers import TicketDetail_for_admin, manager_list_serializer, Employee_list_serializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import json
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .permissions import *
from datetime import date

logger = logging.getLogger(__name__)

##Admin
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """
    Authenticate an admin and return a token if credentials are valid.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None and hasattr(user,'admin'):
            token, created = Token.objects.get_or_create(user=user)
            logger.info(f"Admin {user.username} logged in successfully.")
            return JsonResponse({'status': 'success', 'token': token.key})
        logger.warning(f"Failed login attempt for username: {data['username']}")
        return JsonResponse({'status': 'failed', 'message': 'Invalid credentials'}, status=401)
    logger.error("Invalid request method for admin_login")
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)
  
@api_view(["GET"])
@permission_classes([IsAdmin])
def view_dashboard_admin(request):
    """
    View the admin dashboard with all ticket details.
    """
    try:
        leave_requests = TicketDetails.objects.filter()
        serializer = TicketDetail_for_admin(leave_requests, many=True)
        logger.info("Admin dashboard viewed successfully.")
        return Response(serializer.data, status=HTTP_200_OK)
    except TicketDetails.DoesNotExist:
        logger.warning("No ticket requests found for admin dashboard.")
        return Response({"error": "No requests found"}, status=HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAdmin])
def manage_managers(request):
    """
    Manage managers with GET and POST methods.
    Handles manager retrieval and creation.
    """
    if request.method == 'GET':
        try:
            manager_list = Manager.objects.all()
            serializer = manager_list_serializer(manager_list, many=True)
            logger.info("Manager list retrieved successfully.")
            return Response(serializer.data, status=HTTP_200_OK)
        except Manager.DoesNotExist:
            logger.warning("No managers found.")
            return Response({"error": "No managers found"}, status=HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            if not all([username, password]):
                logger.warning("Manager creation failed due to missing fields.")
                return Response({
                    'status': 'failed', 
                    'message': 'All fields are required'
                }, status=HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            
            manager = Manager.objects.create(
                username=username,
                user=user,
                email = email
            )
            send_mail(
            'Travel Partner Account created',
            f'{username}, you accounted is created successfully, Manager id is {user.manager.id}.',
            'admin@example.com',
            [user.manager.email],
            fail_silently=False,
            )
            logger.info(f"Manager {username} created successfully.")
            return Response({
                'status': 'success', 
                'data': {
                    'username': username, 
                }
            }, status=HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error creating manager: {str(e)}")
            return Response({
                'status': 'failed', 
                'message': str(e)
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
@permission_classes([IsAdmin])
def manage_employees(request):
    """
    Manage employees with GET and POST methods.
    Handles employee retrieval and creation.
    """
    if request.method == 'GET':
        try:
            employee_list = Employee.objects.all()
            serializer = Employee_list_serializer(employee_list, many=True)
            logger.info("Employee list retrieved successfully.")
            return Response(serializer.data, status=HTTP_200_OK)
        except Employee.DoesNotExist:
            logger.warning("No employees found.")
            return Response({"error": "No employees found"}, status=HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')
            date_of_joining = str(date.today())
            manager_id = data.get('manager_id')
            email = data.get('email')
            
            if not all([username, password, manager_id]):
                logger.warning("Employee creation failed due to missing fields.")
                return Response({
                    'status': 'failed', 
                    'message': 'All fields are required'
                }, status=HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            
            employee = Employee.objects.create(
                username=username,
                date_of_joining=date_of_joining,
                manager_id=manager_id,
                email = email,
                user=user
            )
            
            send_mail(
            'Travel Partner Account created',
            f'{username}, you accounted is created successfully, Employee id is {user.employee.id}.',
            'admin@example.com',
            [user.employee.email],
            fail_silently=False,
            )
            logger.info(f"Employee {username} created successfully.")
            return Response({
                'status': 'success', 
                'data': {
                    'username': username, 
                }
            }, status=HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating employee: {str(e)}")
            return Response({
                'status': 'failed', 
                'message': str(e)
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAdmin])
def close_ticket(request):
    """
    Close a ticket by setting its status to 'Close'.
    """
    if request.method == 'PUT':
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')
        try:
            ticket = TicketDetails.objects.get(id=ticket_id)
            ticket.admin_ticket_status = "Close"
            ticket.save()
            logger.info(f"Ticket {ticket_id} closed successfully.")
            return JsonResponse({'status': 'success', 'message': 'Ticket closed successfully'})
        except TicketDetails.DoesNotExist:
            logger.warning(f"Ticket {ticket_id} not found.")
            return JsonResponse({'status': 'failed', 'message': 'Ticket not found'}, status=404)
    logger.error("Invalid request method for close_ticket")
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAdmin])
def approve_ticket_admin(request):
    """
    Approve a ticket by an admin and send a notification email.
    """
    if request.method == 'PUT':
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')
        feedback = data.get('feedback', '')     
        ticket = TicketDetails.objects.get(id=ticket_id)
        ticket.manager_ticket_status = "Approved"
        ticket.additional_request_admin = feedback
        ticket.save()
        send_mail(
            'Ticket Approved by Admin',
            f'Your ticket with ID {ticket_id} has been approved by the admin.',
            'admin@example.com',
            [ticket.employee.email],
            fail_silently=False,
        )
        logger.info(f"Ticket {ticket_id} approved successfully.")
        return JsonResponse({
            'status': 'success', 
            'message': 'Ticket approved successfully',
            'feedback': feedback
        })
    logger.error("Invalid request method for approve_ticket_admin")
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)
