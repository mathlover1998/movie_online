from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
# router.register(r'password',ChangePasswordViewSet, basename='password')
urlpatterns = [
    path('', include(router.urls)),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('check-user/',CurrentUserView.as_view(),name='check'),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
    # path('change-password/',change_password,name='change_password'),
]