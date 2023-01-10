from django.urls import path
 
from .views import MovieListView,upload_file,MoviesShows,TheatreShows,BookingInit,BookSeats,AllMovies,SearchCity,formset_view
urlpatterns = [
    path('movie_list/', AllMovies.as_view(),name='movies'),
    path('movies/<str:city_id>/', MovieListView.as_view(),name='movies_in_city'),
    path('upload_movie_detail/', upload_file),
    path('MovieShows/<str:movie_id>/<str:city_id>/<str:date>/',MoviesShows.as_view()),
    path('current_in_theatre/<str:cinema_hall>/<str:city_id>/<str:date>/', TheatreShows.as_view() ,name="current_movies_in_theatre"),
    path('booking_initialization/<str:city_name>/<str:time>/<str:hall>/<str:movie_name>/<str:date>/<str:total_seats_bookig>/', BookingInit.as_view(),name='booking_initialization'),
    path('ticket_booking/', BookSeats.as_view(),name='ticket_booking'),
    path('search_city/<str:city_name>/', SearchCity.as_view(),name='search_city'),
    path('booking/', formset_view,name='booking'),
]   