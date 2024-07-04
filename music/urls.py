from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout/',views.logout,name="logout"),
    path('music/<str:song_name>/',views.music,name="music"),
    path('search/',views.search,name="search"),
    path ('song_list/<str:al>/',views.song_list,name="songs")
]
