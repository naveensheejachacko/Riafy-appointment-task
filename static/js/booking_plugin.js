(function() {
    // Create and inject CSS
    const style = document.createElement('style');
    style.textContent = `
        .booking-container {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .booking-header {
            text-align: center;
            margin-bottom: 20px;
        }
        .booking-form-group {
            margin-bottom: 15px;
        }
        .booking-label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .booking-input, .booking-select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .booking-slots {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }
        .booking-slot {
            padding: 8px 12px;
            background-color: #e9f5ff;
            border: 1px solid #b8dcff;
            border-radius: 4px;
            cursor: pointer;
        }
        .booking-slot.selected {
            background-color: #007bff;
            color: white;
            border-color: #0056b3;
        }
        .booking-slot.disabled {
            background-color: #f5f5f5;
            color: #aaa;
            cursor: not-allowed;
            border-color: #ddd;
        }
        .booking-btn {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
        }
        .booking-btn:hover {
            background-color: #0056b3;
        }
        .booking-btn:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        .booking-message {
            margin-top: 20px;
            padding: 10px;
            border-radius: 4px;
            text-align: center;
        }
        .booking-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .booking-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    `;
    document.head.appendChild(style);

    // Create the booking form HTML
    function createBookingWidget(targetElementId, apiBaseUrl) {
        // Default API URL if not provided
        apiBaseUrl = apiBaseUrl || '';
        
        const targetElement = document.getElementById(targetElementId);
        if (!targetElement) {
            console.error(`Element with ID "${targetElementId}" not found`);
            return;
        }

        const today = new Date();
        const formattedDate = today.toISOString().split('T')[0];

        targetElement.innerHTML = `
            <div class="booking-container">
                <div class="booking-header">
                    <h2>Book an Appointment</h2>
                </div>
                <form id="booking-form">
                    <div class="booking-form-group">
                        <label class="booking-label" for="booking-name">Name</label>
                        <input class="booking-input" type="text" id="booking-name" name="name" required>
                    </div>
                    <div class="booking-form-group">
                        <label class="booking-label" for="booking-phone">Phone Number</label>
                        <input class="booking-input" type="tel" id="booking-phone" name="phone_number" pattern="[0-9+]+" required>
                    </div>
                    <div class="booking-form-group">
                        <label class="booking-label" for="booking-date">Date</label>
                        <input class="booking-input" type="date" id="booking-date" name="date" min="${formattedDate}" required>
                    </div>
                    <div class="booking-form-group">
                        <label class="booking-label">Available Time Slots</label>
                        <div id="booking-available-slots" class="booking-slots">
                            <p>Select a date to see available time slots</p>
                        </div>
                        <input type="hidden" id="booking-time-slot" name="time_slot">
                    </div>
                    <button type="submit" class="booking-btn" id="booking-submit-btn" disabled>Book Appointment</button>
                </form>
                <div id="booking-message" class="booking-message" style="display: none;"></div>
            </div>
        `;

        // Add event listeners
        const dateInput = document.getElementById('booking-date');
        const slotsContainer = document.getElementById('booking-available-slots');
        const form = document.getElementById('booking-form');
        const submitButton = document.getElementById('booking-submit-btn');
        const messageDiv = document.getElementById('booking-message');

        // Fetch available slots when date changes
        dateInput.addEventListener('change', function() {
            fetchAvailableSlots(dateInput.value);
        });

        // Handle form submission
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            bookAppointment();
        });

        // Function to fetch available slots
        function fetchAvailableSlots(date) {
            slotsContainer.innerHTML = '<p>Loading available slots...</p>';
            
            fetch(`${apiBaseUrl}/api/v1/available-slots/?date=${date}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    
                    if (data.available_slots && data.available_slots.length > 0) {
                        renderTimeSlots(data.available_slots);
                    } else {
                        slotsContainer.innerHTML = '<p>No available slots for this date</p>';
                        submitButton.disabled = true;
                    }
                })
                .catch(error => {
                    slotsContainer.innerHTML = `<p>Error: ${error.message}</p>`;
                    submitButton.disabled = true;
                });
        }

        // Function to render time slots
        function renderTimeSlots(slots) {
            slotsContainer.innerHTML = '';
            slots.forEach(slot => {
                const slotElement = document.createElement('div');
                slotElement.className = 'booking-slot';
                slotElement.textContent = slot;
                slotElement.addEventListener('click', function() {
                    // Remove selected class from all slots
                    document.querySelectorAll('.booking-slot').forEach(el => {
                        el.classList.remove('selected');
                    });
                    
                    // Add selected class to clicked slot
                    slotElement.classList.add('selected');
                    
                    // Set the hidden input value
                    document.getElementById('booking-time-slot').value = slot;
                    
                    // Enable submit button
                    submitButton.disabled = false;
                });
                slotsContainer.appendChild(slotElement);
            });
        }

        // Function to book appointment
        function bookAppointment() {
            const formData = {
                name: document.getElementById('booking-name').value,
                phone_number: document.getElementById('booking-phone').value,
                date: document.getElementById('booking-date').value,
                time_slot: document.getElementById('booking-time-slot').value
            };

            submitButton.disabled = true;
            submitButton.textContent = 'Booking...';
            
            fetch(`${apiBaseUrl}/api/v1/book-appointment/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showMessage(data.error, false);
                } else {
                    showMessage('Appointment booked successfully!', true);
                    form.reset();
                    slotsContainer.innerHTML = '<p>Select a date to see available time slots</p>';
                }
                submitButton.textContent = 'Book Appointment';
                submitButton.disabled = true;
            })
            .catch(error => {
                showMessage(`Error: ${error.message}`, false);
                submitButton.textContent = 'Book Appointment';
                submitButton.disabled = false;
            });
        }

        // Function to show messages
        function showMessage(text, isSuccess) {
            messageDiv.textContent = text;
            messageDiv.style.display = 'block';
            
            if (isSuccess) {
                messageDiv.className = 'booking-message booking-success';
            } else {
                messageDiv.className = 'booking-message booking-error';
            }
            
            // Hide message after 5 seconds
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        }
    }

    // Expose the function to global scope
    window.initAppointmentBooking = function(targetElementId, apiBaseUrl) {
        createBookingWidget(targetElementId, apiBaseUrl);
    };
})();