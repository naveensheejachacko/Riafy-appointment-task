# booking/tests/test_api.py
import pytest
import json
from datetime import date
from django.urls import reverse
from booking.models import Appointment

@pytest.mark.django_db
class TestAvailableSlotsAPI:
    
    def test_get_available_slots(self, client):
        """Test fetching available slots for a date"""
        url = reverse('available_slots') + '?date=2025-03-15'
        response = client.get(url)
        
        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'available_slots' in content
        
        # Verify we have the expected number of slots (10AM-5PM, 30min intervals, excluding 1-2PM)
        # That's 10:00, 10:30, 11:00, 11:30, 12:00, 12:30, 2:00, 2:30, 3:00, 3:30, 4:00, 4:30 = 12 slots
        assert len(content['available_slots']) == 12
        
        # Check for specific time slots
        assert "10:00 AM" in content['available_slots']
        assert "04:30 PM" in content['available_slots']
        
        # Check that lunch break is excluded
        assert "01:00 PM" not in content['available_slots']
        assert "01:30 PM" not in content['available_slots']
    
    def test_booked_slots_not_available(self, client):
        """Test that booked slots don't appear as available"""
        # Create a booking
        Appointment.objects.create(
            name="Test User",
            phone_number="1234567890", 
            date=date(2025, 3, 15),
            time_slot="10:00 AM"
        )
        
        # Check available slots
        url = reverse('available_slots') + '?date=2025-03-15'
        response = client.get(url)
        
        assert response.status_code == 200
        content = json.loads(response.content)
        
        # The booked slot should not be available
        assert "10:00 AM" not in content['available_slots']
        
        # Other slots should still be available
        assert "10:30 AM" in content['available_slots']

@pytest.mark.django_db
class TestBookAppointmentAPI:
    
    def test_book_appointment_success(self, client):
        """Test successful appointment booking"""
        url = reverse('book_appointment')
        data = {
            "name": "Test User",
            "phone_number": "1234567890",
            "date": "2025-03-15",
            "time_slot": "10:00 AM"
        }
        
        response = client.post(
            url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        content = json.loads(response.content)
        assert content['success'] is True
        
        # Verify appointment was created in the database
        appointment = Appointment.objects.get(name="Test User")
        assert appointment.time_slot == "10:00 AM"
    
    def test_book_appointment_missing_fields(self, client):
        """Test booking with missing fields"""
        url = reverse('book_appointment')
        data = {
            "name": "Test User",
            # Missing phone_number
            "date": "2025-03-15",
            "time_slot": "10:00 AM"
        }
        
        response = client.post(
            url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        content = json.loads(response.content)
        assert 'error' in content
    
    def test_double_booking_prevented(self, client):
        """Test that double booking is prevented"""
        # Create first booking
        Appointment.objects.create(
            name="Test User 1",
            phone_number="1234567890", 
            date=date(2025, 3, 15),
            time_slot="10:00 AM"
        )
        
        # Try to book the same slot
        url = reverse('book_appointment')
        data = {
            "name": "Test User 2",
            "phone_number": "0987654321",
            "date": "2025-03-15",
            "time_slot": "10:00 AM"
        }
        
        response = client.post(
            url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        content = json.loads(response.content)
        assert 'error' in content
        assert 'already booked' in content['error']