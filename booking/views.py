from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from .models import Appointment

@swagger_auto_schema(
    methods=['get'],
    manual_parameters=[
        openapi.Parameter(
            'date',
            openapi.IN_QUERY,
            description="Date in YYYY-MM-DD format",
            type=openapi.TYPE_STRING,
            required=True,
            example="2024-03-09"
        )
    ],
    responses={
        200: openapi.Response(
            description="List of available time slots",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'available_slots': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING)
                    )
                }
            )
        ),
        400: openapi.Response(
            description="Bad request",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    }
)
@api_view(['GET'])
def get_available_slots(request):
    """
    Retrieve available appointment slots for a specific date.

    Parameters:
    - request: HTTP GET request with 'date' parameter (YYYY-MM-DD format)

    Returns:
    - JsonResponse with available time slots
    - Time slots are between 10:00 AM and 5:00 PM, excluding lunch hour (1:00-2:00 PM)
    - Each slot is 30 minutes long

    Example Response:
    {
        "available_slots": ["10:00 AM", "10:30 AM", "11:00 AM", ...]
    }

    Error Response:
    {
        "error": "error message"
    }
    """
    date_str = request.query_params.get('date')
    if not date_str:
        return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Parse the date
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Generate all possible slots (10:00 AM to 5:00 PM, excluding 1:00-2:00 PM)
        all_slots = []
        current_time = datetime.strptime("10:00 AM", "%I:%M %p")
        end_time = datetime.strptime("5:00 PM", "%I:%M %p")
        
        while current_time < end_time:
            # Skip lunch break (1:00 PM to 2:00 PM)
            time_str = current_time.strftime('%I:%M %p')
            if not (time_str == "01:00 PM" or time_str == "01:30 PM"):
                all_slots.append(time_str)
            
            # Add 30 minutes
            current_time = current_time + timedelta(minutes=30)
        
        # Get booked slots for the selected date
        booked_appointments = Appointment.objects.filter(date=selected_date)
        booked_slots = [appointment.time_slot for appointment in booked_appointments]
        
        # Filter out booked slots
        available_slots = [slot for slot in all_slots if slot not in booked_slots]
        
        return Response({'available_slots': available_slots})
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'phone_number', 'date', 'time_slot'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, example="John Doe"),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example="+1234567890"),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format='date', example="2025-03-09"),
            'time_slot': openapi.Schema(type=openapi.TYPE_STRING, example="10:00 AM"),
        }
    ),
    responses={
        200: openapi.Response(
            description="Appointment booked successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'appointment_id': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            )
        ),
        400: openapi.Response(
            description="Bad request",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    }
)
@api_view(['POST'])
@csrf_exempt
def book_appointment(request):
    """
    Book a new appointment.

    Parameters:
    - request: HTTP POST request with JSON body containing:
        - name: string
        - phone_number: string
        - date: string (YYYY-MM-DD format)
        - time_slot: string (hh:mm AM/PM format)

    Returns:
    - JsonResponse with booking confirmation
    
    Success Response:
    {
        "success": true,
        "message": "Appointment booked successfully",
        "appointment_id": 123
    }

    Error Response:
    {
        "error": "error message"
    }
    """
    try:
        data = request.data
        name = data.get('name')
        phone_number = data.get('phone_number')
        date_str = data.get('date')
        time_slot = data.get('time_slot')
        
        # Validate required fields
        if not all([name, phone_number, date_str, time_slot]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse date
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Validate time slot
        is_valid, error_message = is_valid_time_slot(time_slot)
        if not is_valid:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if slot is already booked
        if Appointment.objects.filter(date=date, time_slot=time_slot).exists():
            return Response({'error': 'This slot is already booked'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create appointment
        appointment = Appointment(
            name=name,
            phone_number=phone_number,
            date=date,
            time_slot=time_slot
        )
        appointment.save()
        
        return Response({
            'success': True,
            'message': 'Appointment booked successfully',
            'appointment_id': appointment.id
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def is_valid_time_slot(time_slot):
    """Validate if the time slot is within business hours."""
    try:
        # Convert time slot string to datetime object for comparison
        slot_time = datetime.strptime(time_slot, '%I:%M %p')
        
        # Define business hours
        business_start = datetime.strptime('10:00 AM', '%I:%M %p')
        business_end = datetime.strptime('5:00 PM', '%I:%M %p')
        lunch_start = datetime.strptime('1:00 PM', '%I:%M %p')
        lunch_end = datetime.strptime('2:00 PM', '%I:%M %p')
        
        # Check if time is within business hours
        if not (business_start <= slot_time < business_end):
            return False, "Appointments are only available between 10:00 AM and 5:00 PM"
            
        # Check if time is during lunch break
        if lunch_start <= slot_time < lunch_end:
            return False, "Appointments are not available during lunch hour (1:00 PM - 2:00 PM)"
            
        # Check if time is at 30-minute intervals
        minutes = slot_time.hour * 60 + slot_time.minute
        if minutes % 30 != 0:
            return False, "Appointments must be scheduled at 30-minute intervals"
            
        return True, ""
    except ValueError:
        return False, "Invalid time format. Please use format like '10:00 AM'"