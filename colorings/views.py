from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Author, ColoringBook, Markers
from .serializers import AuthorSerializer, Coloring_BookSerializer, MarkersSerializer

class AuthorList(APIView):
    """
    List all authors 
    """
    def get(self, request):
        Authors = Author.objects.all()
        serializer = AuthorSerializer(Authors, many=True)
        return Response(serializer.data)
    
class Coloring_BooksList(APIView):
    """
    List all coloring books
    """
    def get(self, request):
        Coloring_Books = ColoringBook.objects.all()
        serializer = Coloring_BookSerializer(Coloring_Books, many=True)
        return Response(serializer.data)
    
class MarkersList(APIView):
    """
    List all possible boxes of markers
    """
    def get(self, request):
        markers = Markers.objects.all()
        serializer = MarkersSerializer(markers, many=True)
        return Response(serializer.data)