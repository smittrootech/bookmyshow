from django.urls import path
 
# importing views from views..py
from .views import MovieListView,upload_file,MoviesShows,TheatreShows,BookingInit
urlpatterns = [
    path('movies/<int:city_id>/', MovieListView.as_view(),name='movies_in_city'),
    path('upload_movie_detail/', upload_file),
    path('MovieShows/<int:movie_id>/<int:city_id>/<str:date>/',MoviesShows.as_view()),
    path('current_in_theatre/<str:cinema_hall>/<str:city_id>/<str:date>/', TheatreShows.as_view() ,name="current_movies_in_theatre"),
    path('booking_initialization/<str:city_name>/<str:time>/<str:hall>/<str:movie_name>/<str:date>/', BookingInit.as_view(),name='booking_initialization')
]   