from rest_framework import serializers
from .models import Author, ColoringBook, Markers  

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography']


class Coloring_BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all()) #combine them with one author
    class Meta:
        model = ColoringBook 
        fields = ['id', 'title', 'author', 'theme', 'price', 'description']

class MarkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markers
        fields = ['id', 'name', 'brand', 'price']
