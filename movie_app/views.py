from rest_framework.views import APIView
from .serializers import MovieSerializer
from .models import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsSuperUserOrReadOnly
from django.shortcuts import render
from .documents import MovieDocument
from elasticsearch_dsl.query import MultiMatch


def index(request):
    q = request.GET.get('q')
    context = {}
    if q:
        query = MultiMatch(query =q, fields = ['title','synopsis'],fuzziness = 'AUTO')
        movies = MovieDocument.search().query(query)
        context['movies'] = movies
    return render(request,'index.html',context)


class MovieView(APIView):
    permission_classes =[IsSuperUserOrReadOnly]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     elif self.request.method =='POST':
    #         return [IsAuthenticated()]
    #     return super().get_permissions()
    
    def get(self,request,end_point=None):
        if end_point:
            try:
                movie = Movie.objects.get(end_point=end_point)
                serializer = MovieSerializer(movie)
                return Response(serializer.data)
            except Movie.DoesNotExist:
                return Response({'msg':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            title = request.query_params.get('q')
            sort_by =request.query_params.get('sort_by','-release_date')
            search = MovieDocument.search()
            if title:
                search = search.query("match",title=title)
            else:
                search = search.query("match_all")
            search = search.sort(sort_by)
            movies = search.to_queryset()
            serializer = MovieSerializer(movies,many=True)
            return Response(serializer.data)
    
    def post(self,request):
        serializer =  MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)




class MovieGenreView(APIView):
    pass