# travel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import TravelOption, Booking, City
from .forms import BookingForm, TravelSearchForm
from .serializers import TravelOptionSerializer, BookingSerializer

from django.shortcuts import render
from .models import TravelOption, City  # Assuming you have a City model

def travel_list(request):
    # Fetch all available cities from the City model
    cities = City.objects.all()

    # Fetch all travel options
    travel_options = TravelOption.objects.all()

    # Instantiate the search form with the GET parameters
    form = TravelSearchForm(request.GET)

    # Filter the travel options based on form input
    if form.is_valid():
        travel_type = form.cleaned_data.get('travel_type')
        source = form.cleaned_data.get('source')
        destination = form.cleaned_data.get('destination')
        date = form.cleaned_data.get('date')
        sort_by = form.cleaned_data.get('sort_by')

        if travel_type:
            travel_options = travel_options.filter(type=travel_type)
        if source:
            travel_options = travel_options.filter(source__name__icontains=source)
        if destination:
            travel_options = travel_options.filter(destination__name__icontains=destination)
        if date:
            travel_options = travel_options.filter(date_time__date=date)

        if sort_by:
            travel_options = travel_options.order_by(sort_by)

    # Render the travel list template and pass cities and form
    return render(request, 'travel/travel_list.html', {
        'travel_options': travel_options,
        'form': form,
        'cities': cities  # Pass the cities to the template
    })


def travel_detail(request, pk):
    travel_option = get_object_or_404(TravelOption, pk=pk)
    return render(request, 'travel/travel_detail.html', {'travel_option': travel_option})

@login_required
def booking_create(request, travel_id):
    travel_option = get_object_or_404(TravelOption, pk=travel_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if booking.number_of_seats > travel_option.available_seats:
                messages.warning(request, f"Only {travel_option.available_seats} seats are available. Your request for {booking.number_of_seats} seats exceeds this limit.")
                return render(request, 'travel/booking_form.html', {'form': form, 'travel_option': travel_option})
           
            booking.user = request.user
            booking.travel_option = travel_option
            booking.total_price = travel_option.price * booking.number_of_seats
            booking.booking_id = f"B{Booking.objects.count() + 1:06d}"
            booking.save()
            travel_option.available_seats -= booking.number_of_seats
            travel_option.save()
            messages.success(request, "Booking created successfully!")
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'travel/booking_form.html', {'form': form, 'travel_option': travel_option})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'travel/booking_list.html', {'bookings': bookings})

class TravelOptionViewSet(viewsets.ModelViewSet):
    queryset = TravelOption.objects.all()
    serializer_class = TravelOptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'source', 'destination', 'date_time']

    def get_queryset(self):
        queryset = TravelOption.objects.all()
        travel_type = self.request.query_params.get('type', None)
        source = self.request.query_params.get('source', None)
        destination = self.request.query_params.get('destination', None)
        date = self.request.query_params.get('date', None)
        sort_by = self.request.query_params.get('sort_by', None)

        if travel_type:
            queryset = queryset.filter(type=travel_type)
        if source:
            queryset = queryset.filter(source__name__icontains=source)
        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)
        if date:
            queryset = queryset.filter(date_time__date=date)
        if sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status == 'CONFIRMED':
            booking.status = 'CANCELLED'
            booking.save()
            booking.travel_option.available_seats += booking.number_of_seats
            booking.travel_option.save()
            return Response({'status': 'Booking cancelled'})
        return Response({'status': 'Booking cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)

