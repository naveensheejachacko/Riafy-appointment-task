# Appointment Booking System

A simple appointment booking system built with Django and JavaScript, featuring a modern UI and RESTful API.

## Features

- Easy-to-use appointment booking interface
- Available time slot management
- RESTful API with Swagger documentation
- Responsive design
- Form validation
- Success/error notifications

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/naveensheejachacko/Riafy-appointment-task.git
cd appointment_system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On linux
source venv/bin/activate  
# On Windows: 
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the application:
- Main application: http://127.0.0.1:8000/
- Admin interface: http://127.0.0.1:8000/admin/
- API documentation: http://127.0.0.1:8000/swagger/

## API Endpoints

- GET `/api/v1/available-slots/`: Get available time slots for a specific date
- POST `/api/v1/book-appointment/`: Book a new appointment

## Using the Booking Widget

Include the booking plugin in your HTML:

```html
<div id="booking-widget"></div>
<script src="/static/js/booking_plugin.js"></script>
<script>
    initAppointmentBooking('booking-widget', 'http://your-api-base-url');
</script>
```

## Development

The project structure is organized as follows:

```
appointment_system/
├── appointment_system/  # Project settings
├── booking/            # Main application
├── static/            # Static files
│   └── js/
│       └── booking_plugin.js
└── templates/         # HTML templates
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

![Screenshot 2025-03-09 114510](https://github.com/user-attachments/assets/f5bd8537-42da-4a31-8444-7e685de90453)
![Screenshot 2025-03-09 114503](https://github.com/user-attachments/assets/70c5966c-44a2-4693-8bf0-90f51757ca1e)
![Screenshot 2025-03-09 114353](https://github.com/user-attachments/assets/9bf62b22-91c6-446a-9bb3-92e255ec14e8)



