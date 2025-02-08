# Urls.py file for accounts app
from django.urls import path
from .views import login_view, logout_view, home_view, create_user


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create_user/', create_user, name='create_user'),
]