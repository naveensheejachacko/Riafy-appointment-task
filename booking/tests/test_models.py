# booking/tests/test_models.py
import pytest
from django.db.utils import IntegrityError
from datetime import date
from booking.models import Appointment

@pytest.mark.django_db
class TestAppointmentModel:
    
    def test_create_appointment(self):
        """Test that an appointment can be created with valid data"""
        appointment = Appointment.objects.create(
            name="Test User",
            phone_number="1234567890",
            date=date(2025, 3, 15),
            time_slot="10:00 AM"
        )
        assert appointment.id is not None
        assert appointment.name == "Test User"
        assert appointment.phone_number == "1234567890"
        assert appointment.date == date(2025, 3, 15)
        assert appointment.time_slot == "10:00 AM"
    
    def test_prevent_double_booking(self):
        """Test that the same time slot cannot be booked twice on the same date"""
        # Create first appointment
        Appointment.objects.create(
            name="Test User 1",
            phone_number="1234567890",
            date=date(2025, 3, 15),
            time_slot="10:00 AM"
        )
        
        # Try to create second appointment for same slot
        with pytest.raises(IntegrityError):
            Appointment.objects.create(
                name="Test User 2",
                phone_number="0987654321",
                date=date(2025, 3, 15),
                time_slot="10:00 AM"
            )
    
    def test_different_dates_same_slot(self):
        """Test that the same time slot can be booked on different dates"""
        # Create appointment for first date
        Appointment.objects.create(
            name="Test User 1",
            phone_number="1234567890",
            date=date(2025, 3, 15),
            time_slot="10:00 AM"
        )
        
        # Create appointment for second date
        appointment2 = Appointment.objects.create(
            name="Test User 2",
            phone_number="0987654321",
            date=date(2025, 3, 16),
            time_slot="10:00 AM"
        )
        
        assert appointment2.id is not None