# travel/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    # Add this new line for the OTP verification page
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('', views.travel_options, name='travel_options'),
    path('book/<int:travel_id>/', views.book_travel, name='book_travel'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    # --- Add this new URL for the cancellation OTP verification ---
    path('cancel-booking-verify/', views.cancel_booking_verify, name='cancel_booking_verify'),
    path('payment-success/', views.payment_success, name='payment_success'),
]