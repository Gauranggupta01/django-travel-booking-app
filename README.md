# Travel Booking Web Application

A full-featured travel booking web application built with Python and the Django framework. Users can register, browse travel options, book tickets with Razorpay integration, and manage their bookings.

## Features

- **User Authentication:** Secure user registration, login (with OTP), and profile management.
- **Travel Listings:** Browse and filter flights, trains, and buses.
- **Booking System:** Book tickets and view booking history.
- **Payment Integration:** Secure payments handled via Razorpay (Cards, UPI, QR Code).
- **Security:** OTP verification for both login and booking cancellations.
- **Responsive UI:** Modern user interface built with Bootstrap that works on all devices.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/django-travel-booking-app.git
    cd django-travel-booking-app
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv env
    # On Windows
    env\Scripts\activate
    # On macOS/Linux
    source env/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your environment variables** in `settings.py`:
    -   `SECRET_KEY`
    -   `RAZORPAY_KEY_ID` & `RAZORPAY_KEY_SECRET`
    -   Email backend settings for production.

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
