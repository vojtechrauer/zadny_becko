from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, Film, Director, Review, FavoriteFilm

class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        labels = {
            'username': 'Přezdívka',
            'email': 'E-mail'
        }

class UpdateUser(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_pic']


class CreateFilm(ModelForm):
    class Meta:
        model = Film
        fields = ['title', 'image', 'director', 'summary']
        labels = {
            'title': 'Název filmu',
            'image': 'Plakát',
            'director': 'Režisér',
            'summary': 'Popis'
        }


class CreateDirector(ModelForm):
    class Meta:
        model = Director
        fields = '__all__'
        exclude = ['slug']
        labels = {
            'name': 'Jméno',
            'bio': 'Životopis',
            'image': 'Foto'
        }

class CreateReview(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        exclude = ['author', 'slug']
        labels = {
            'title': 'Název',
            'body': '',
            'image': 'Titulní fotografie',
            'rating': 'Počet hvězdiček'
        }

class AddFilmToFavorites(ModelForm):
    class Meta:
        model = FavoriteFilm
        exclude = '__all__'