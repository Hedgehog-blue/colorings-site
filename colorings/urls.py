from django.urls import path 
from colorings.views import AuthorList, Coloring_BooksList, MarkersList

urlpatterns = [
    path('authors/', AuthorList.as_view()),
    path('colorings/', Coloring_BooksList.as_view()),
    path('markers/', MarkersList.as_view()),
]

