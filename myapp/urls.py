from .views import registration_view, login_view, logout_view, home, search_users, post_create, my_profile
from django.urls import path

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'), 
    path('search_users/', search_users, name='search_users'),
    path('post_create/', post_create, name='post_create'),
    path('my_profile/', my_profile, name='my_profile'),    
    path('', home, name='home'),
]
