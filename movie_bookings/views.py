import json
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.db.models import CharField
from django.db.models.functions import Lower
CharField.register_lookup(Lower)
from .models import Movies,Show
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
import datetime
from django.views.decorators.csrf import csrf_exempt
import itertools
from .models import CinemaSeats,CinemaHall,Show,City
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import MoviesDetailForm,CinemaHallForm
from django.forms import formset_factory


def formset_view(request):
    context ={}
  
    # creating a formset
    cinemabookformset = formset_factory(CinemaHallForm)
    formset = cinemabookformset()
      
    # Add the formset to context dictionary
    context['formset']= formset
    return render(request, "movie_bookings/booking.html", context)

class AllMovies(View):
    def get(self, request): 
        upcoming_movies=Movies.objects.filter(release_date__gte=datetime.datetime.now())
        current_movies=Movies.objects.filter(release_date__lte=datetime.datetime.now())
        return render(request,'movie_bookings/bookmyshow.html',{"current_movies":current_movies,"upcoming_movies":upcoming_movies})


def upload_file(request):
    if request.method == 'POST':
        form = MoviesDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('MovieListView')
    else:
        form = MoviesDetailForm()
    return render(request, 'movie_bookings/movies.html', {'form': form})

class MovieListView(View):
    def get(self, request,city_id):
        
        movies=Movies.objects.filter(city__name=city_id)
        date= datetime.datetime.now().date()
        return render(request,'movie_bookings/movies_list.html',{"object_list":movies,"city_id":city_id,"date":str(date)})


class MoviesShows(View):
     def get(self, request, movie_id,city_id,date):
        try:
            try:
                abc=Show.objects.filter(movie__id=movie_id).filter(city__name=city_id,date=date)
            except:
                abc=Show.objects.filter(movie__title=movie_id).filter(city__name=city_id,date=date)
            movie_name,city_name=(abc.first().movie.title,abc.first().city.name)
           
            shows={}
            for i in abc:
                if i.cinema_hall.name not in shows:
                    shows[i.cinema_hall.name] = [{str(i.start_time):i.price}]
                else:
                    shows[i.cinema_hall.name] += [{str(i.start_time):i.price}]
            return render(request,'movie_bookings/buytickets.html',{'context':shows,'city':city_id ,'movie_name':movie_name ,'city_name':city_name,'date':str(date)})

        except Exception as e:
            return redirect('movies_in_city', city_id=city_id)
        
        
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class TheatreShows(View):
    def get(self, request,cinema_hall,city_id,date):
        current_movies=Show.objects.filter(cinema_hall__name=cinema_hall
        ).filter(city__name=city_id,date=date)
        shows={}
        for i in current_movies:
            if i.movie.title not in shows:
                shows[i.movie.title] = [{str(i.start_time):str(i.price)}]
            else:
                shows[i.movie.title] += [{str(i.start_time):str(i.price)}]
    
        return JsonResponse({'data':shows}, safe=False)

class BookingInit(View):

    def get(self,request,city_name,time,hall,movie_name,date,total_seats_bookig):

        try:
                city_name=City.objects.filter(id=city_name).first().name
        except:
                pass
        city_name=City.objects.get(name=city_name) 
        show_time=Show.objects.get(start_time=time,date=date,cinema_hall__name=hall)

        cinema_booking=CinemaSeats.objects.filter(show_time=show_time,cinema_hall__name=hall,movie_name__title=movie_name,city__name=city_name)

        seats=[(i.booked_seats) for i in cinema_booking]
        total_seats_booked=list(itertools.chain.from_iterable(seats))
        cinema_hall=CinemaHall.objects.get(name=hall,city__name=city_name)


        if len(total_seats_booked)==0:
            total_seats_booked=["None"]
       
        show=Show.objects.get(start_time=time,date=date,cinema_hall__name=hall,movie__title=movie_name)
        return render(request, 'movie_bookings/seat_booking.html', {'city_name': city_name,"time":time,"cinema_hall":hall,"movie_name":movie_name,"date":date,"total_seats_bookig":total_seats_bookig,"price":show.price,"total_rows":cinema_hall.total_seats//10,'total_seats_booked':total_seats_booked})

class SearchCity(View):

    def get(self,request,city_name):
        
        search_result=city_name=City.objects.filter(name__icontains=city_name.lower())
        search_result=[i.name for i in search_result]
        return JsonResponse({'search_result':search_result}, safe=False)


class BookSeats(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BookSeats, self).dispatch(request, *args, **kwargs)
  
    def post(self,request):
        # import pdb;pdb.set_trace()
        # print(">>>>>>>",request)
        data=json.load(request)
        city_name=data['city_name']
        time=data['time']
        cinema_hall=data['hall']
        movie_name=data['movie']
        date=data['date']
        total_seats_bookig=data['total_seats_bookig']
        payable_amount=data['payable_amount']
        selected_total_seats=data['selected_total_seats']
        amount_paid=data["is_paid"]
        total_seats_bookig =total_seats_bookig

        if not isinstance(selected_total_seats,list):
            selected_total_seats=selected_total_seats.split(",")
        try:
            city_name=City.objects.filter(id=city_name).first().name
        except:
            pass
        city_name=City.objects.get(name=city_name)
        cinema_hall=CinemaHall.objects.get(name=cinema_hall,city__name=city_name)
        movie_name=Movies.objects.get(title=movie_name)
        show_time=Show.objects.get(start_time=time,date=date,cinema_hall__name=cinema_hall)

        if amount_paid:
            events = CinemaSeats.objects.filter(seatnumber=total_seats_bookig,type="GOLD",show_time=show_time,cinema_hall=cinema_hall,movie_name=movie_name,city=city_name,final_price=payable_amount,booked_seats=selected_total_seats)
            events.update(amount_paid=True)
            obj = Show.objects.get(cinema_hall__name=cinema_hall,movie__title=movie_name,start_time=str(show_time.start_time),city__name=city_name,date=date)
            booked_seats=len(selected_total_seats)
            obj.total_seats=obj.total_seats-booked_seats
            obj.save()

        elif selected_total_seats[1]=="Revert_seats":
            selected_total_seats=selected_total_seats[0].split(",")
            events = CinemaSeats.objects.filter(seatnumber=total_seats_bookig,type="GOLD",show_time=show_time,cinema_hall=cinema_hall,movie_name=movie_name,city=city_name,final_price=payable_amount,booked_seats=selected_total_seats)
            events.delete()

        else:
        
            cinema_booking=CinemaSeats(seatnumber=total_seats_bookig,type="GOLD",show_time=show_time,cinema_hall=cinema_hall,movie_name=movie_name,city=city_name,final_price=payable_amount,booked_seats=selected_total_seats)
            cinema_booking.save()
           

        return JsonResponse(data,safe=False)

    def get(self,request):

        city_name=request.GET.get('city_name')
        time=request.GET.get('time')
        cinema_hall=request.GET.get('cinema_hall')
        movie_name=request.GET.get('movie_name')
        date=request.GET.get('date')
        total_seats_bookig=request.GET.get('total_seats_bookig')
        payable_amount=int(request.GET.get('payable_amount'))
        selected_total_seats=request.GET.get('selected_total_seats')
        current_time=request.GET.get('current_time')
        convenience_fees= int((0.18)*payable_amount) + payable_amount

        return render(request,'movie_bookings/payment_page.html',{"city_name":city_name,"selected_total_seats":selected_total_seats,"payable_amount":payable_amount,"convenience_fees":convenience_fees,"time":time,"cinema_hall":cinema_hall,"movie_name":movie_name,"date":date,"total_seats_bookig":total_seats_bookig,"current_time":current_time})

