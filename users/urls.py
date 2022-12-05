from django.urls import path
from .views import UserRegistration,home,UserLogin,UserLogout


from users import views as user_views

urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegistration, name='register'),
    path('login/', UserLogin, name='login'),
    path('logout/', UserLogout, name='logout'),
]
