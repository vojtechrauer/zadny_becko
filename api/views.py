from django.shortcuts import render
from rest_framework import generics
from blog.models import Film
from .serializers import FilmSerializer
# Create your views here.

class FilmList(generics.ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class FilmCreate(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    def post(self, request, *args, **kwargs):
        film = Film.objects.create(
            request.POST.data
        )


