from django.db import models
from PIL import Image
import os
from datetime import datetime, timedelta
import datetime as datetime

from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class City(models.Model):

    name=models.CharField(max_length=200)
    State=models.CharField(max_length=200)
    zipcode=models.IntegerField()

    def __str__(self):
        return self.name


class Movies(models.Model):

    title=models.CharField(max_length=200)
    description=models.CharField(max_length=200,null=True,blank=True)
    language=models.CharField(max_length=200)
    duration=models.DurationField(null=True,blank=True)
    release_date=models.DateField()
    country=models.CharField(max_length=200)
    Genre=models.CharField(max_length=200)
    movie_image_url=models.ImageField(upload_to='movie_bookings/static/', blank=True,
                              null=True, editable=True)
    movie_image=models.CharField(null=True,blank=True,max_length=200)
    city=models.ManyToManyField(City,related_name='movies_in_city', blank=True,null=True)

    def __str__(self):  
        return self.title

    def save(self, *args, **kwargs):
        
        if self.movie_image_url:
            self.movie_image = str(self.movie_image_url).split("/")[-1]
        return super().save(*args, **kwargs)

class CinemaHall(models.Model):

    name=models.CharField(max_length=200)
    total_seats=models.IntegerField(default=0)
    city=models.ForeignKey(City,on_delete=models.CASCADE,related_name='city', blank=True,null=True)

    def __str__(self):
        return self.name 


class Show(models.Model):

    date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField (blank=True,null=True)
    language=models.CharField(max_length=200)
    total_seats=models.IntegerField(default=0)
    cinema_hall= models.ForeignKey(CinemaHall,on_delete=models.CASCADE,related_name='show_in_cinema', blank=True,null=True)
    movie=models.ForeignKey(Movies,on_delete=models.CASCADE,related_name='movie', blank=True,null=True)
    city=models.ForeignKey(City,on_delete=models.CASCADE,related_name='city_name', blank=True,null=True)
    price=models.FloatField(default=0)

    def __str__(self):
        return str(self.date)+ " " +str(self.start_time)

    def save(self, *args, **kwargs):



        if self.start_time and not self.end_time :

            duration = Movies.objects.filter(title=self.movie.title).first()
            (h, m, s) = str(self.start_time).split(':')
            seconds=duration.duration.total_seconds()
            hours = seconds // 3600.
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            self.end_time=str(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))+datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds)))   
                        
            time = Show.objects.filter(cinema_hall=self.cinema_hall).values('start_time','end_time','date')
            times=[i for i in time]
            values=[]
            for time in times:
                values.append(tuple(time.values()))
            for i in values:
                if self.start_time >= i[0] and self.start_time <= i[1] and i[2]==self.date:
                     raise ValidationError("already have movie between this slot in th hall ") 
                else:
                    continue

            self.total_seats=CinemaHall.objects.filter(name=self.cinema_hall,city__name=self.city).first().total_seats

        return super().save(*args, **kwargs)


class CinemaSeats(models.Model):

    class SeatType(models.TextChoices):
        Gold = 'Gold', _('Gold')
        Silver = 'Silver', _('Silver')

    seatnumber=models.IntegerField(default=0)
    booked_seats = ArrayField(models.CharField(max_length=200), blank=True,null=True)
    type=models.CharField(max_length=20,choices=SeatType.choices)
    cinema_hall= models.ForeignKey(CinemaHall,on_delete=models.CASCADE,related_name='cinema_hall',null=True,blank=True)
    movie_name=models.ForeignKey(Movies,on_delete=models.CASCADE,related_name='selected_movie',null=True,blank=True)
    show_time=models.ForeignKey(Show,on_delete=models.CASCADE,related_name='selected_movie_show_time',null=True,blank=True)
    city=models.ForeignKey(City,on_delete=models.CASCADE,related_name='city_name_for_booking', blank=True,null=True)
    final_price=models.FloatField(default=0)

    def __str__(self):
        return str(self.movie_name)
