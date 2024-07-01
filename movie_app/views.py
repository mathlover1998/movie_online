from django.http import JsonResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Added Successfully')
    
    def update(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Updated Successfully')
    
    def destroy(self, request):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('Deleted Successfully')
    
