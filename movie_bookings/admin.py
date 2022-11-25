from django.contrib import admin
from .models import Movies,Show,CinemaHall,CinemaSeats,City

# Register your models here.


admin.site.register(Movies)
admin.site.register(Show)
admin.site.register(CinemaHall)
admin.site.register(CinemaSeats)
admin.site.register(City)
