from django.urls import path
from .views import *

urlpatterns = [
    path('',MovieView.as_view(),name='movie'),
    path('search/',index,name='search'),
    path('genre/',GenreView.as_view(),name='genre_list'),
    path('genre/<str:name>/',GenreView.as_view(),name='genre_detail'),
    path('cast/',CastView.as_view(),name='cast_detail')
    
]