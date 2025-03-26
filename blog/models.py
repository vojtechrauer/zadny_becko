from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field

# Custom user model extending Django's AbstractUser
class User(AbstractUser): 
    class Meta:
        verbose_name = 'Uživatel'  # Singular name for the admin panel
        verbose_name_plural = 'Uživatelé'  # Plural name for the admin panel

    email = models.EmailField(unique=True)  # Email field, must be unique
    username = models.CharField(max_length=200, unique=True)  # Username field, must be unique
    profile_pic = models.ImageField(
        default='/profile_pics/default_profile_pic.png',  # Default profile picture
        upload_to='profile_pics/'  # Directory to upload profile pictures
    )
    USERNAME_FIELD = 'email'  # Set email as the unique identifier for authentication
    REQUIRED_FIELDS = ['username']  # Fields required when creating a user via the command line

    def __str__(self):
        return self.username  # String representation of the user

# Model representing a director
class Director(models.Model): 
    class Meta:
        verbose_name = 'Režisér'  # Singular name for the admin panel
        verbose_name_plural = 'Režiséři'  # Plural name for the admin panel

    name = models.CharField(max_length=200)  # Name of the director
    slug = models.SlugField(unique=True)  # Unique slug for the director
    bio = models.TextField()  # Biography of the director
    image = models.ImageField(
        upload_to='directors/',  # Directory to upload director images
        default='directors/dummy_portrait.png',  # Default image
        blank=True, null=True  # Allow blank or null values
    )

    def __str__(self):
        return self.name  # String representation of the director

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generate slug from the director's name
        super().save(*args, **kwargs)

# Model representing a film
class Film(models.Model): 
    class Meta:
        verbose_name = 'Film'  # Singular name for the admin panel
        verbose_name_plural = 'Filmy'  # Plural name for the admin panel

    title = models.CharField(max_length=200)  # Title of the film
    slug = models.SlugField(unique=True)  # Unique slug for the film
    image = models.ImageField(
        upload_to='posters/',  # Directory to upload film posters
        default='posters/dummy_poster.png',  # Default poster
        blank=True, null=True  # Allow blank or null values
    )
    director = models.ForeignKey(
        Director,  # Link to the Director model
        null=True,  # Allow null values
        on_delete=models.SET_NULL  # Set to null if the director is deleted
    )
    summary = models.TextField()  # Summary of the film
    tags = TaggableManager(blank=True)  # Tags for the film, optional

    def __str__(self):
        return self.title  # String representation of the film

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug from the film's title
        super().save(*args, **kwargs)

# Model representing a user's favorite films
class FavoriteFilm(models.Model): 
    user = models.ForeignKey(
        User,  # Link to the User model
        on_delete=models.CASCADE,  # Delete the favorite film if the user is deleted
        related_name='favorite_films'  # Related name for reverse lookup
    )
    film = models.ForeignKey(
        Film,  # Link to the Film model
        on_delete=models.CASCADE,  # Delete the favorite film if the film is deleted
        related_name='in_favorites'  # Related name for reverse lookup
    )

    class Meta:
        unique_together = ('user', 'film')  # Ensure a user cannot favorite the same film multiple times

# Model representing a film review
class Review(models.Model): 
    class Meta:
        verbose_name = 'Recenze'  # Singular name for the admin panel
        verbose_name_plural = 'Recenze'  # Plural name for the admin panel

    class Rating(models.IntegerChoices): 
        # Choices for the rating field with integer values and their UI representations
        A = 5, '5 ⭐'
        B = 4, '4 ⭐'
        C = 3, '3 ⭐'
        D = 2, '2 ⭐'
        E = 1, '1 ⭐'
        F = 0, '0 ⭐'

    title = models.CharField(max_length=200)  # Title of the review
    slug = models.SlugField(unique=True)  # Unique slug for the review
    film = models.ForeignKey(
        Film,  # Link to the Film model
        on_delete=models.CASCADE  # Delete the review if the film is deleted
    )
    body = CKEditor5Field('Text', config_name='extends')  # Rich text field for the review body
    author = models.ForeignKey(
        User,  # Link to the User model
        on_delete=models.CASCADE  # Delete the review if the author is deleted
    )
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when the review is created
    edited = models.DateTimeField(auto_now=True)  # Timestamp when the review is last edited
    image = models.ImageField(
        upload_to='review_headers/',  # Directory to upload review header images
        default='review_headers/dummy_header.png',  # Default header image
        blank=True, null=True  # Allow blank or null values
    )
    rating = models.IntegerField(
        choices=Rating.choices  # Rating choices for the review
    )

    def __str__(self):
        return self.title  # String representation of the review

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug from the review's title
        super().save(*args, **kwargs)

# Model representing a comment on a review
class Comment(models.Model): 
    class Meta:
        verbose_name = 'Komentář'  # Singular name for the admin panel
        verbose_name_plural = 'Komentáře'  # Plural name for the admin panel

    user = models.ForeignKey(
        User,  # Link to the User model
        on_delete=models.CASCADE  # Delete the comment if the user is deleted
    )
    review = models.ForeignKey(
        Review,  # Link to the Review model
        on_delete=models.CASCADE  # Delete the comment if the review is deleted
    )
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment is created
    edited = models.DateTimeField(auto_now=True)  # Timestamp when the comment is last edited
    body = models.TextField()  # Body of the comment
