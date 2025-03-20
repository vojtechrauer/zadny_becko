from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field

class User(AbstractUser): #class representing a user
    class Meta:
        verbose_name = 'Uživatel'
        verbose_name_plural = 'Uživatelé'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200, unique=True)
    profile_pic = models.ImageField(
        default='/profile_pics/default_profile_pic.png',
        upload_to='profile_pics/')

    """"""
    USERNAME_FIELD = 'email' #setting the login username to email
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Director(models.Model): #class representing a director
    class Meta:
        verbose_name = 'Režisér'
        verbose_name_plural = 'Režiséři'

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    bio = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) #returns the slug dynamically created from the director's name
            super().save(*args, **kwargs)


class Film(models.Model): #class representing a film
    class Meta:
        verbose_name = 'Film'
        verbose_name_plural = 'Filmy'

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='posters/', default='posters/dummy_poster.png', blank=True, null=True) #if the film poster wasn't added by user, a default dummy poster is provided
    director = models.ForeignKey(Director, null=True, on_delete=models.SET_NULL) #linking the Film class to the Director class
    summary = models.TextField()
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) #returns the slug dynamically created from the film's title
        super().save(*args, **kwargs)

class FavoriteFilm(models.Model): #helper class defining links between users and their favorite films
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_films')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='in_favorites')

    class Meta:
        unique_together = ('user', 'film') #setting values 'user' and 'film' to be unique together to avoid adding a film to the favorites more than once


class Review(models.Model): #class representing a film review
    class Meta:
        verbose_name = 'Recenze'
        verbose_name_plural = 'Recenze'

    class Rating(models.IntegerChoices): #choices for field 'rating' with integer values and respectively their UI representations
        A = 5, '5 ⭐'
        B = 4, '4 ⭐'
        C = 3, '3 ⭐'
        D = 2, '2 ⭐'
        E = 1, '1 ⭐'
        F = 0, '0 ⭐'

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    body = CKEditor5Field('Text', config_name='extends') #ck-editor field enabling user to further format the text of their review
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='review_headers/', default='review_headers/dummy_header.png', blank=True, null=True)
    rating = models.IntegerField(
        choices=Rating.choices
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) #returns the slug dynamically created from the review's title
        super().save(*args, **kwargs)

class Comment(models.Model): #class representing a comment
    class Meta:
        verbose_name = 'Komentář'
        verbose_name_plural = 'Komentáře'

    user = models.ForeignKey(User, on_delete=models.CASCADE) #link to the user who created the comment
    review = models.ForeignKey(Review, on_delete=models.CASCADE) #link to the review that is commented
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    body = models.TextField()
