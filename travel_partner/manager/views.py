from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.permissions import AllowAny
from travel_app.models import TicketDetails
from .serializers import  TicketDetail_for_manager
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import json
from django.core.mail import send_mail
from .permissions import *
import logging

logger = logging.getLogger(__name__)

##Manager       
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def manager_login(request):
    """
    Authenticate a manager and return a token if credentials are valid.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None and hasattr(user,'manager'):
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'status': 'success', 'token': token.key})
        return JsonResponse({'status': 'failed', 'message': 'Invalid credentials'}, status=401)
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

@api_view(["GET"])
@permission_classes([IsManager])
def view_dashboard_manager(request):
    """
    View the manager dashboard with all ticket details for the manager.
    """
    logger.info(f"Manager {request.user.manager.id} is viewing the dashboard.")
    try:
        leave_requests = TicketDetails.objects.filter(manager_id=request.user.manager.id)
        serializer = TicketDetail_for_manager(leave_requests, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except TicketDetails.DoesNotExist:
        logger.warning(f"No ticket requests found for manager {request.user.manager.id}.")
        return Response({"error": "No requests found"}, status=HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error while fetching dashboard for manager {request.user.manager.id}: {str(e)}")
        return Response({"error": str(e)}, status=400)

@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsManager])
def approve_ticket_manager(request, ticket_id):
    """
    Approve a ticket by a manager and send a notification email.
    """
    if request.method == 'PUT':
        feedback = request.data.get('feedback', '')     
        ticket = TicketDetails.objects.get(id=ticket_id)
        ticket.manager_ticket_status = "Approved"
        ticket.additional_request_manager = feedback
        ticket.save()
        logger.info(f"Manager {request.user.manager.id} approved ticket {ticket_id}.")
        send_mail(
            'Ticket Approved by Manager',
            f'Your ticket with ID {ticket_id} has been approved by the manager.',
            'manager@example.com',
            [ticket.employee.email],
            fail_silently=False,
        )
        return JsonResponse({
            'status': 'success', 
            'message': 'Ticket approved successfully',
            'feedback': feedback
        })
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)   

@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsManager])
def reject_ticket(request, ticket_id):
    """
    Reject a ticket by a manager and send a notification email.
    """
    if request.method == 'PUT':
        feedback = request.data.get('feedback', '')    
        ticket = TicketDetails.objects.get(id=ticket_id)
        ticket.manager_ticket_status = "Rejected"
        ticket.additional_request_admin = feedback
        ticket.save()
        try:
            res = send_mail(
                'Ticket Rejected',
                f'Your ticket with ID {ticket_id} has been rejected.',
                'admin@example.com',
                [ticket.employee.email],
                fail_silently=False,
            )
            logger.info(f"Manager {request.user.manager.id} rejected ticket {ticket_id}. Email sent successfully.")
        except Exception as e:
            logger.error(f"Manager {request.user.manager.id} rejected ticket {ticket_id}. Email failed to send: {str(e)}")
        return JsonResponse({
            'status': 'success', 
            'message': 'Ticket rejected successfully',
            'feedback': feedback
        })
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
@api_view(["GET"])
@permission_classes([IsManager])
def filter_dash(request):
    """
    Filter dashboard records based on date, place, and status.
    """
    if request.method == "GET":
        start_date = request.GET.get("startDate")
        end_date = request.GET.get("endDate")
        place = request.GET.get("place")
        status = request.GET.get("status")
        records = TicketDetails.objects.filter(manager_id=request.user.manager.id) 
        if start_date:
            records = records.filter(date__gte=start_date)
        if end_date:
            records = records.filter(date__lte=end_date)
        if place:
            records = records.filter(place__icontains=place)
        if status:
            records = records.filter(status=status)
        data = list(records.values())  
        return JsonResponse({"records": data})
    return JsonResponse({"error": "Invalid request"}, status=400)