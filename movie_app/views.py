# from django.http import JsonResponse
# from rest_framework import viewsets,status,generics
# from rest_framework.views import APIView
# from .models import *
# from .serializers import *
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# # Create your views here.

# class DirectorViewSet(viewsets.ModelViewSet):
#     queryset = Director.objects.all()
#     serializer_class = DirectorSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('Added Successfully')
    
#     def update(self, request):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('Updated Successfully')
    
#     def destroy(self, request):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response('Deleted Successfully')


# class MovieView(APIView):
#     permission_classes = (IsAuthenticated,)
#     def get(self,request,pk=None):
#         if pk:
#             try:
#                 movie = Movie.objects.get(pk=pk)
#                 serializer = MovieSerializer(movie)
#                 return Response(serializer.data,status=status.HTTP_200_OK)
#             except Movie.DoesNotExist:
#                 return Response(status=status.HTTP_404_NOT_FOUND)
#         else:
#             movies = Movie.objects.all()
#             serializer = MovieSerializer(movies,many=True)
#             return Response(serializer.data,status=status.HTTP_200_OK)
#     def post(self,request):
#         serializer = MovieSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(status=status.HTTP_201_CREATED)
#     def put(self,request,pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         partial = request.method =='PATCH'
#         serializer = MovieSerializer(movie,data=request.data,partial=partial)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     def delete(self,request,pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # class MovieListCreate(generics.ListCreateAPIView):
# #     queryset = Movie.objects.all()
# #     serializer_class = MovieSerializer
# #     permission_classes = [IsAuthenticated]

# # class MovieRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Movie.objects.all()
# #     serializer_class = MovieSerializer
# #     permission_classes = [IsAuthenticated]

# class CountryListCreate(generics.ListCreateAPIView):
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer
#     permission_classes = [IsAuthenticated]

# class CountryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer
#     permission_classes = [IsAuthenticated]

# # class 