from django.urls import path
from . import views

urlpatterns = [
    path('movie/list', views.FilmList.as_view(), name='film-list'),
    path('movie/create', views.FilmCreate.as_view(), name='film-create')
]