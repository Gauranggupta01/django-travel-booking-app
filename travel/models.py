from django.db import models
from django.contrib.auth.models import User

class TravelOption(models.Model):
    # ... (this model remains the same) ...
    TRAVEL_TYPES = (
        ('Flight', 'Flight'),
        ('Train', 'Train'),
        ('Bus', 'Bus'),
    )
    travel_id = models.AutoField(primary_key=True)
    travel_type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    image = models.ImageField(upload_to='travel_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.travel_type} from {self.source} to {self.destination}"


class Booking(models.Model):
    BOOKING_STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )

    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='Pending')
    
    # Add fields for Razorpay
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.username}"