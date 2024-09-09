from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name

class TravelOption(models.Model):
    TRAVEL_TYPES = (
        ('FLIGHT', 'Flight'),
        ('TRAIN', 'Train'),
        ('BUS', 'Bus'),
    )
    travel_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    # These ForeignKey fields will create 'source_id' and 'destination_id' in the database
    source = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='arrivals')
    date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.get_type_display()} - {self.source} to {self.destination}"

class Booking(models.Model):
    BOOKING_STATUS = (
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )
    booking_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='CONFIRMED')

    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.username}"
    