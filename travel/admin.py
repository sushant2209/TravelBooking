from django.contrib import admin
from .models import TravelOption, Booking,City

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ('travel_id', 'type', 'source', 'destination', 'date_time', 'price', 'available_seats')
    list_filter = ('type', 'source', 'destination')
    search_fields = ('travel_id', 'source', 'destination')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'travel_option', 'number_of_seats', 'total_price', 'booking_date', 'status')
    list_filter = ('status', 'travel_option__type')
    search_fields = ('booking_id', 'user__username', 'travel_option__travel_id')
    raw_id_fields = ('user', 'travel_option')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
