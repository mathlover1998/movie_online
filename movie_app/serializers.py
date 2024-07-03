# from .models import *
# from rest_framework import serializers


# class MovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         exclude = ['end_point']

# class DirectorSerializer(serializers.ModelSerializer):
#     movies = MovieSerializer(many=True,read_only=True)
#     class Meta:
#         model = Director
#         depth = 1
#         fields = ['id','name','date_of_birth','movies']

# class CountrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Country
#         fields = '__all__'


# class RateMovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rate
#         fields = '__all__'