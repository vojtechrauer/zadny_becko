from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

class User(AbstractUser):
    class Meta:
        verbose_name = 'Uživatel'
        verbose_name_plural = 'Uživatelé'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200, unique=True)
    profile_pic = models.ImageField(
        default='/profile_pics/default_profile_pic.png',
        upload_to='profile_pics/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Director(models.Model):
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
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)


class Film(models.Model):
    class Meta:
        verbose_name = 'Film'
        verbose_name_plural = 'Filmy'

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='posters/')
    director = models.ForeignKey(Director, null=True, on_delete=models.SET_NULL)
    summary = models.TextField()
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class FavoriteFilm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_films')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='in_favorites')

    class Meta:
        unique_together = ('user', 'film')


class Review(models.Model):
    class Meta:
        verbose_name = 'Recenze'
        verbose_name_plural = 'Recenze'

    class Rating(models.IntegerChoices):
        A = 5, '5 ⭐'
        B = 4, '4 ⭐'
        C = 3, '3 ⭐'
        D = 2, '2 ⭐'
        E = 1, '1 ⭐'
        F = 0, '0 ⭐'

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True)
    rating = models.IntegerField(
        choices=Rating.choices
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.image:
            self.image = self.film.image
        super().save(*args, **kwargs)

class Comment(models.Model):
    class Meta:
        verbose_name = 'Komentář'
        verbose_name_plural = 'Komentáře'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    body = models.TextField()
