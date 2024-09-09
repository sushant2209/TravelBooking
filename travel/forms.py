# travel/forms.py
from django import forms
from .models import Booking, City,TravelOption

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats']

class TravelSearchForm(forms.Form):
    TRAVEL_TYPE_CHOICES = TravelOption.TRAVEL_TYPES
    SORT_CHOICES = [
        ('price', 'Price'),
        ('date_time', 'Date/Time'),
    ]

    travel_type = forms.ChoiceField(choices=TRAVEL_TYPE_CHOICES, required=False)
    source = forms.CharField(required=False, widget=forms.Select(attrs={'class': 'city-select'}))
    destination = forms.CharField(required=False, widget=forms.Select(attrs={'class': 'city-select'}))
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)
