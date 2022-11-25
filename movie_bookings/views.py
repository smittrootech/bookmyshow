from django.shortcuts import render
from django.shortcuts import redirect



from .models import Movies,Show
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
import datetime


from .models import CinemaSeats,CinemaHall,Show,City
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import MoviesDetailForm,SeatBooking


def upload_file(request):
    if request.method == 'POST':
        form = MoviesDetailForm(request.POST, request.FILES)
        print(form.data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('MovieListView')
    else:
        form = MoviesDetailForm()
    return render(request, 'movie_bookings/movies.html', {'form': form})

class MovieListView(View):
    def get(self, request,city_id):
        movies=Movies.objects.filter(city__id=city_id)
        date= datetime.datetime.now().date()
        return render(request,'movie_bookings/movies_list.html',{"object_list":movies,"city_id":city_id,"date":str(date)})


class MoviesShows(View):
     def get(self, request, movie_id,city_id,date):
        try:
            abc=Show.objects.filter(movie__id=movie_id).filter(city__id=city_id,date=date)
            movie_name,city_name=(abc.first().movie.title,abc.first().city.name)
            shows={}
            for i in abc:
                if i.cinema_hall.name not in shows:
                    shows[i.cinema_hall.name] = [i.start_time]
                else:
                    shows[i.cinema_hall.name] += [i.start_time]
            return render(request,'movie_bookings/buytickets.html',{'context':shows,'city':city_id ,'movie_name':movie_name ,'city_name':city_name,'date':date})

        except:
            return redirect('movies_in_city', city_id=city_id)
        
        
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class TheatreShows(View):
    def get(self, request,cinema_hall,city_id,date):
        if is_ajax(request=request):
            print("abc")
            current_movies=Show.objects.filter(cinema_hall__name=cinema_hall).filter(city__id=city_id,date=date)
            shows={}
            for i in current_movies:
                if i.movie.title not in shows:
                    shows[i.movie.title] = [i.start_time]
                else:
                    shows[i.movie.title] += [i.start_time]
            return JsonResponse({'data':shows}, safe=False)

class BookingInit(View):
    def post(self,request,city_name,time,hall,movie_name,date):

            # create a form instance and populate it with data from the request:
        form = SeatBooking(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            seatnumber=request.POST.get('seatnumber')
            type=request.POST.get('type')
            show_time=time
            movie_name=movie_name
            city_name=city_name
            date=date
            try:
                city_name=City.objects.filter(id=city_name).first().name
            except:
                pass

            cinema_hall=CinemaHall.objects.get(name=hall)
            movie_name=Movies.objects.get(title=movie_name)
            show_time=Show.objects.get(start_time=show_time,date=date)
            city=City.objects.get(name=city_name) 
            cinema_booking=CinemaSeats(seatnumber=seatnumber,type=type,show_time=show_time,cinema_hall=cinema_hall,movie_name=movie_name,city=city)
            cinema_booking.save()
            obj = Show.objects.get(cinema_hall__name=cinema_hall,movie__title=movie_name,start_time=str(show_time),city__name=city,date=date)
            obj.total_seats=obj.total_seats-1
            print(obj.total_seats)
            obj.save()

            return HttpResponseRedirect('/thanks/')

       
        return render(request, 'movie_bookings/booking.html', {'form': form})

    def get(self,request,city_name,time,hall,movie_name,date):
        form = SeatBooking()

        return render(request, 'movie_bookings/booking.html', {'form': form})
        