# travel/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import TravelOption, Booking
from django.contrib import messages
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import razorpay

# --- Import your custom forms ---
from .forms import CustomUserCreationForm, UserProfileForm, BookingForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully! Please log in to verify your account.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'travel/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            otp = ''.join(random.choices(string.digits, k=6))
            
            subject = 'Your OTP for TravelBook Login'
            message = f'Hi {user.username}, your One-Time Password is: {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            
            request.session['otp'] = otp
            request.session['user_pk_for_otp'] = user.pk
            
            messages.success(request, f"An OTP has been sent to your email: {user.email}")
            return redirect('otp_verify')
    else:
        form = AuthenticationForm()
    return render(request, 'travel/login.html', {'form': form})

def otp_verify(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        
        if entered_otp == stored_otp:
            user_pk = request.session.get('user_pk_for_otp')
            user = User.objects.get(pk=user_pk)
            login(request, user)
            
            del request.session['otp']
            del request.session['user_pk_for_otp']
            
            messages.success(request, "Login successful!")
            return redirect('travel_options')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('otp_verify')
            
    return render(request, 'travel/otp_verify.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'travel/profile.html', {'form': form})
@login_required
def travel_options(request):
    options = TravelOption.objects.all()
    travel_type = request.GET.get('type')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    date = request.GET.get('date')

    if travel_type:
        options = options.filter(travel_type=travel_type)
    if source:
        options = options.filter(source__icontains=source)
    if destination:
        options = options.filter(destination__icontains=destination)
    if date:
        options = options.filter(date_time__date=date)

    return render(request, 'travel/travel_options.html', {'options': options})

@login_required
def book_travel(request, travel_id):
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            num_seats = form.cleaned_data['number_of_seats']
            if num_seats > travel_option.available_seats:
                messages.error(request, 'Not enough available seats.')
                return render(request, 'travel/book_travel.html', {'form': form, 'travel_option': travel_option})

            booking = form.save(commit=False)
            booking.user = request.user
            booking.travel_option = travel_option
            booking.total_price = travel_option.price * num_seats
            booking.save()

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            amount = int(booking.total_price * 100)
            
            order_data = {
                "amount": amount,
                "currency": "INR",
                "receipt": f"booking_{booking.booking_id}",
            }
            
            razorpay_order = client.order.create(data=order_data)
            booking.razorpay_order_id = razorpay_order['id']
            booking.save()
            
            # --- FIX: Pass the 'booking' object to the template ---
            context = {
                'booking': booking, # This was missing
                'razorpay_order': razorpay_order,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': amount
            }
            return render(request, 'travel/checkout.html', context)
    else:
        form = BookingForm()

    return render(request, 'travel/book_travel.html', {'form': form, 'travel_option': travel_option})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'travel/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    if booking.status != 'Confirmed':
        messages.error(request, "This booking cannot be cancelled.")
        return redirect('my_bookings')

    otp = ''.join(random.choices(string.digits, k=6))
    subject = 'Your OTP for Booking Cancellation'
    message = f'Hi {request.user.username}, your One-Time Password to cancel your booking is: {otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [request.user.email])
    
    request.session['cancel_otp'] = otp
    request.session['booking_id_for_cancel'] = booking_id
    
    messages.info(request, "An OTP has been sent to your email to confirm the cancellation.")
    return redirect('cancel_booking_verify')

def cancel_booking_verify(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('cancel_otp')
        booking_id = request.session.get('booking_id_for_cancel')

        if not stored_otp or not booking_id:
            messages.error(request, "Session expired. Please try again.")
            return redirect('my_bookings')

        if entered_otp == stored_otp:
            booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
            
            booking.status = 'Cancelled'
            booking.travel_option.available_seats += booking.number_of_seats
            booking.travel_option.save()
            booking.save()
            
            del request.session['cancel_otp']
            del request.session['booking_id_for_cancel']
            
            messages.success(request, 'Booking cancelled successfully.')
            return redirect('my_bookings')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('cancel_booking_verify')
            
    return render(request, 'travel/cancel_booking_verify.html')

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            client.utility.verify_payment_signature(params_dict)
            booking = Booking.objects.get(razorpay_order_id=order_id)
            booking.razorpay_payment_id = payment_id
            booking.razorpay_signature = signature
            booking.status = 'Confirmed'
            booking.save()
            travel_option = booking.travel_option
            travel_option.available_seats -= booking.number_of_seats
            travel_option.save()
            messages.success(request, "Your payment was successful and booking is confirmed!")
            return render(request, 'travel/payment_success.html')
        except Exception as e:
            messages.error(request, f"Payment verification failed: {e}")
            return redirect('my_bookings')
    return redirect('my_bookings')
