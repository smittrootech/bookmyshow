from django import forms
from .models import Movies,CinemaSeats,CinemaHall
from django.contrib.auth.password_validation import validate_password



class MoviesDetailForm(forms.ModelForm):

    class Meta:
        model = Movies
        fields = '__all__'

class SeatBooking(forms.ModelForm):

    class Meta:
        model=CinemaSeats
        fields=['seatnumber','type']


class CinemaHallForm(forms.ModelForm):

    class Meta:
        model=CinemaHall
        fields='__all__'




    