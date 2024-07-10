from django.urls import path
from .views import *

urlpatterns = [
    path('',MovieView.as_view(),name='movie'),
    path('search/',index,name='search')
]