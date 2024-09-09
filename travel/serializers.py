from rest_framework import serializers
from .models import TravelOption, Booking

class TravelOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelOption
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('booking_id', 'user', 'total_price', 'booking_date', 'status')

    def create(self, validated_data):
        user = self.context['request'].user
        travel_option = validated_data['travel_option']
        number_of_seats = validated_data['number_of_seats']

        if number_of_seats > travel_option.available_seats:
            raise serializers.ValidationError("Not enough seats available.")

        total_price = travel_option.price * number_of_seats
        booking = Booking.objects.create(
            user=user,
            travel_option=travel_option,
            number_of_seats=number_of_seats,
            total_price=total_price,
            booking_id=f"B{Booking.objects.count() + 1:06d}"
        )

        travel_option.available_seats -= number_of_seats
        travel_option.save()

        return booking