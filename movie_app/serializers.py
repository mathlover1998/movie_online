from .models import *
from rest_framework import serializers

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name',]

class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        exclude = ['id',]
        