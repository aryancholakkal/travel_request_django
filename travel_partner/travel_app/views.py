import logging
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Admin, TicketDetails
from .serializer import  TicketDetail_for_manager
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
import json
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .permissions import *

logger = logging.getLogger(__name__)

##COMMON
@csrf_exempt
@api_view(['POST'])
def user_logout(request):
    logger.info("User logout requested")
    """
    Log out the user and delete their authentication token.
    """
    if request.method == 'POST':
        request.user.auth_token.delete()
        logout(request)
        logger.info("User logged out successfully")
        return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})
    logger.warning("Invalid request method for user logout")
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsManager, IsAdmin])
def request_edit(request):
    logger.info("Request edit initiated")
    """
    Request an edit for a ticket and send a notification email.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')
        feedback = data.get('feedback', '')     
        ticket = TicketDetails.objects.get(id=ticket_id)
        ticket.manager_ticket_status = "Edit Required"
        ticket.additional_request_admin = feedback
        ticket.save()
        send_mail(
            'Ticket Edit Required',
            f'Your ticket with ID {ticket_id} requires edits.',
            'admin@example.com',
            [ticket.employee.user.email],
            fail_silently=False,
        )
        logger.info(f"Edit requested for ticket ID {ticket_id}")
        return JsonResponse({
            'status': 'success', 
            'message': 'Ticket waiting for edit',
            'feedback': feedback
        })
    logger.warning("Invalid request method for request edit")
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsManager, IsAdmin])
def search_records(request):
    logger.info("Search records initiated")
    """
    Search for ticket records based on a query.
    """
    if request.method == "GET":
        query = request.GET.get("query", "")
        
        records = TicketDetails.objects.filter(
            place__icontains=query
        ) | TicketDetails.objects.filter(
            status__icontains=query
        )
        
        data = list(records.values())  
        logger.info(f"Records found for query: {query}")
        return JsonResponse({"records": data})

    logger.warning("Invalid request method for search records")
    return JsonResponse({"error": "Invalid request"}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sort_requests(request):
    logger.info("Sort requests initiated")
    """
    Sort ticket requests based on a specified field.
    """
    sort_by = request.GET.get('sort_by', 'date_of_request')
    try:
        requests = TicketDetails.objects.all().order_by(sort_by)
        serializer = TicketDetail_for_manager(requests, many=True)
        logger.info(f"Requests sorted by {sort_by}")
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error sorting requests: {str(e)}")
        return Response({"error": str(e)}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_by_person(request):
    logger.info("Search by person initiated")
    """
    Search for ticket requests by employee username.
    """
    person_name = request.GET.get('person_name', '')
    try:
        requests = TicketDetails.objects.filter(employee__username__icontains=person_name)
        serializer = TicketDetail_for_manager(requests, many=True)
        logger.info(f"Requests found for person: {person_name}")
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error searching by person: {str(e)}")
        return Response({"error": str(e)}, status=400)  
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_approved_request(request):
    logger.info("Process approved request initiated")
    """
    Process an approved ticket request.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')
        try:
            ticket = TicketDetails.objects.get(id=ticket_id)
            if ticket.manager_ticket_status == "Approved" and ticket.admin_ticket_status == "Approved":
                ticket.admin_ticket_status = "Processed"
                ticket.save()
                logger.info(f"Request processed for ticket ID {ticket_id}")
                return JsonResponse({'status': 'success', 'message': 'Request processed successfully'})
            logger.warning(f"Request not approved by both manager and admin for ticket ID {ticket_id}")
            return JsonResponse({'status': 'failed', 'message': 'Request not approved by both manager and admin'}, status=400)
        except TicketDetails.DoesNotExist:
            logger.error(f"Request not found for ticket ID {ticket_id}")
            return JsonResponse({'status': 'failed', 'message': 'Request not found'}, status=404)
    logger.warning("Invalid request method for process approved request")
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

def send_email(request, subject, message):
    logger.info("Send email initiated")
    """
    Send an email with the given subject and message.
    """
    subject = subject
    from_email = "debugger@gmail.com"
    recipient_list = ["ad;lfad"]
    plain_message = message
    send_mail(subject, plain_message, from_email, recipient_list)
    logger.info("Email sent successfully")
    return Response({"data":'Email sent successfully'})
 
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def add_admin(request):
    logger.info("Add admin initiated")
    """
    Add a new admin user.
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')   
        if not all([username, password]):
            logger.warning("All fields are required for adding admin")
            return JsonResponse({
                'status': 'failed', 
                'message': 'All fields are required'
            }, status=400)
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        admin = Admin.objects.create(
            username=username,
            user = user 
        ) 
        admin.save()       
        logger.info(f"Admin added with username: {username}")
        return JsonResponse({
            'status': 'success', 
            'data': {
                'username': username, 
            }
        })
    except json.JSONDecodeError:
        logger.error("Invalid JSON format for adding admin")
        return JsonResponse({
            'status': 'failed', 
            'message': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        logger.error(f"Error adding admin: {str(e)}")
        return JsonResponse({
            'status': 'failed', 
            'message': str(e)
        }, status=500)
