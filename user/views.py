from rest_framework import status,viewsets,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
import random
from django.core.cache import cache

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data =request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data =request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = get_tokens_for_user(user)
        return Response({
                'token': token,
                }, status=status.HTTP_200_OK)

        
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            print(request.data['access'])
            request.access.delete()
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "password set"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def change_password(request):
#     if request.method=='POST':
#         serializer = ChangePasswordSerializer(data=request.data,context = {'request':request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "password set"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,display_name=None):
        # profile= None
        if display_name:
            profile = get_object_or_404(Profile,display_name=display_name)
        else:
            profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    def put(self,request,display_name=None):
        if display_name and display_name != request.user.profile.display_name:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        profile = request.user.profile
        serializer = ProfileSerializer(instance=profile,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# def update_phone_number(request):
#     if request.method=='GET':
#         serializer = PhoneNumberSerializer(instance=request.user.profile, context = {'request':request})
#         return Response(serializer.data)
#     if request.method =='POST':
#         serializer = PhoneNumberSerializer(data=request.data,context = {'request':request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"status": "phone changed"}, status=status.HTTP_200_OK)


class PhoneNumberChangeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        profile = request.user.profile
        phone_number = profile.phone_number
        return Response({"phone_number": phone_number})
    def post(self,request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            new_phone = serializer.validated_data['new_phone_number']
            otp = str(random.randint(100000, 999999))
            print(otp)
            cache.set(f'{request.user.id}_new_phone_number', new_phone, timeout=300)
            cache.set(f'{request.user.id}_otp',otp,timeout=300)
            return Response({"message": "OTP sent to new phone number"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OTPVerificationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        otp = cache.get(f'{request.user.id}_otp')
        cached_phone_number = cache.get(f'{request.user.id}_new_phone_number')
        return Response({"message": f'{otp}-{cached_phone_number}'},status=status.HTTP_200_OK)
    def post(self,request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            new_phone_number = serializer.validated_data['new_phone_number']
            otp = serializer.validated_data['otp']
            cached_otp = cache.get(f'{request.user.id}_otp')
            cached_phone_number = cache.get(f'{request.user.id}_new_phone_number')
            if cached_phone_number == new_phone_number:
                if cached_otp == otp:
                    profile = request.user.profile
                    profile.phone_number = new_phone_number
                    profile.save()
                    # Clear cache data
                    cache.delete(f'{request.user.id}_new_phone_number')
                    cache.delete(f'{request.user.id}_otp')
                    return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Invalid new phone number"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk=None):
        if pk:
            try:
                address = Address.objects.get(pk=pk,user=request.user)
                serializer = AddressSerializer(address)
                return Response(serializer.data)
            except Address.DoesNotExist:
                return Response({'msg':'Not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            addresses = Address.objects.filter(user=request.user).order_by('-is_default')
            serializer = AddressSerializer(addresses,many=True)
            return Response(serializer.data)
    def post(self,request):
        serializer = AddressSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def put(self,request,pk):
        address = get_object_or_404(Address,pk=pk,user=request.user)
        serializer = AddressSerializer(address,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg":"updated successfully"},status=status.HTTP_205_RESET_CONTENT)
    
    def delete(self,request,pk):
        address = get_object_or_404(Address,pk=pk,user= request.user)
        address.delete()
        return Response({"msg":"delete successfully"},status=status.HTTP_204_NO_CONTENT)
        
