from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'directors',DirectorViewSet,basename='director')
urlpatterns = [
    path('',include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('movies/',MovieView.as_view(),name='movie_list'),
    path('movie/<int:pk>/',MovieView.as_view(),name='movie_detail'),
    # path('movies/',MovieListCreate.as_view(),name='movie_list'),
    # path('movie/<int:pk>/',MovieRetrieveUpdateDestroy.as_view(),name='movie_detail'),
    path('countries/',CountryListCreate.as_view(),name='country_list'),
    path('country/<int:pk>',CountryRetrieveUpdateDestroy.as_view(),name='country_detail')
]