from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, Film, Director, Review, FavoriteFilm
from django_ckeditor_5.widgets import CKEditor5Widget

# Form for user registration, extending Django's UserCreationForm
class RegisterUser(UserCreationForm):
    class Meta:
        model = User  # Use the custom User model
        fields = ['email', 'username', 'password1', 'password2']  # Fields to include in the form
        labels = {  # Custom labels for the form fields
            'username': 'Přezdívka',  # Label for the username field
            'email': 'E-mail'  # Label for the email field
        }

# Form for updating user details
class UpdateUser(ModelForm):
    class Meta:
        model = User  # Use the custom User model
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_pic']  # Fields to include in the form

# Form for creating a new film
class CreateFilm(ModelForm):
    class Meta:
        model = Film  # Use the Film model
        fields = ['title', 'image', 'director', 'summary']  # Fields to include in the form
        labels = {  # Custom labels for the form fields
            'title': 'Název filmu',  # Label for the title field
            'image': 'Plakát',  # Label for the image field
            'director': 'Režisér',  # Label for the director field
            'summary': 'Popis'  # Label for the summary field
        }

# Form for creating a new director
class CreateDirector(ModelForm):
    class Meta:
        model = Director  # Use the Director model
        fields = '__all__'  # Include all fields from the model
        exclude = ['slug']  # Exclude the slug field
        labels = {  # Custom labels for the form fields
            'name': 'Jméno',  # Label for the name field
            'bio': 'Životopis',  # Label for the bio field
            'image': 'Foto'  # Label for the image field
        }

# Form for creating a new review
class CreateReview(ModelForm):
    class Meta:
        model = Review  # Use the Review model
        fields = '__all__'  # Include all fields from the model
        exclude = ['author', 'slug']  # Exclude the author and slug fields
        labels = {  # Custom labels for the form fields
            'title': 'Název',  # Label for the title field
            'body': '',  # No label for the body field
            'image': 'Titulní fotografie',  # Label for the image field
            'rating': 'Počet hvězdiček'  # Label for the rating field
        }
        widgets = {  # Custom widgets for the form fields
            "text": CKEditor5Widget(  # Use CKEditor5 for the text field
                attrs={"class": "django_ckeditor_5"}, config_name="review"  # Widget configuration
            )
        }

# Form for adding a film to a user's favorites
class AddFilmToFavorites(ModelForm):
    class Meta:
        model = FavoriteFilm  # Use the FavoriteFilm model
        exclude = '__all__'  # Exclude all fields (this seems incorrect; likely meant to include fields)