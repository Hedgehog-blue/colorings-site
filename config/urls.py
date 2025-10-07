"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import JsonResponse
from shop.views_index import api_index
from django.urls import path
from shop.views_resources import (
    AuthorsListCreateAPIView, AuthorDetailAPIView,
    ColoringsListCreateAPIView, ColoringDetailAPIView,
    PencilsListCreateAPIView, PencilDetailAPIView
)

urlpatterns = [
    path("", lambda r: JsonResponse({
        "endpoints": {
            "authors": "/authors/",
            "author_detail": "/authors/{id}/",
            "colorings": "/colorings/",
            "coloring_detail": "/colorings/{id}/",
            "pencils": "/pencils/",
            "pencil_detail": "/pencils/{id}/",
        },
        "note": "Use trailing slash.",
    })),
    path("authors/", AuthorsListCreateAPIView.as_view()),
    path("authors/<int:pk>/", AuthorDetailAPIView.as_view()),
    path("colorings/", ColoringsListCreateAPIView.as_view()),
    path("colorings/<int:pk>/", ColoringDetailAPIView.as_view()),
    path("pencils/", PencilsListCreateAPIView.as_view()),
    path("pencils/<int:pk>/", PencilDetailAPIView.as_view()),
]