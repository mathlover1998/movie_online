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
    path('profile/', ProfileView.as_view(), name='my_profile'),
    path('profile/<str:display_name>/', ProfileView.as_view(), name='profile'),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
    path('change-phone-number/', PhoneNumberChangeView.as_view(), name='change-phone-number'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),
]