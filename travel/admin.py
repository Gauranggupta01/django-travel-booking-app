from django.contrib import admin
from .models import TravelOption, Booking

# Customizing the display for the TravelOption model
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ('travel_id', 'travel_type', 'source', 'destination', 'date_time', 'price', 'available_seats')
    list_filter = ('travel_type', 'date_time', 'source', 'destination')
    search_fields = ('source', 'destination')
    list_per_page = 20

# Customizing the display for the Booking model
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'travel_option', 'number_of_seats', 'total_price', 'booking_date', 'status')
    list_filter = ('status', 'booking_date', 'travel_option__travel_type')
    search_fields = ('user__username', 'travel_option__source', 'travel_option__destination')
    list_per_page = 20

# Register your models with the custom admin classes
admin.site.register(TravelOption, TravelOptionAdmin)
admin.site.register(Booking, BookingAdmin)