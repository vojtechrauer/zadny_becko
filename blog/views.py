from django.shortcuts import render, redirect, get_object_or_404
from .models import *  # Import all models
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterUser, CreateFilm, CreateDirector, CreateReview, UpdateUser, AddFilmToFavorites
from taggit.models import Tag
from django.db.models import Avg, Count
from django.core.paginator import Paginator
from django.urls import reverse_lazy

# Function view for resetting a user's password using Django's PasswordResetForm
def reset_password(request):
    form = PasswordResetForm()  # Initialize the password reset form
    context = {'form': form}  # Pass the form to the template
    return render(request, 'blog/user/change_password.html', context)

# Function view for registering a new user
def register_user(request):
    form = RegisterUser()  # Initialize the registration form
    if request.method == 'POST':  # Handle form submission
        form = RegisterUser(request.POST)  # Bind form data
        if form.is_valid():  # Validate the form
            form.save()  # Save the new user

    context = {'form': form}  # Pass the form to the template
    return render(request, 'blog/user/register.html', context)

# Function view for updating user information
@login_required
def update_user(request):
    form_user = UpdateUser(instance=request.user)  # Pre-fill the form with the current user's data
    form_password = PasswordChangeForm(request.user)  # Password change form
    form_reset_password = PasswordResetForm()  # Password reset form

    if request.method == 'POST':  # Handle form submission
        form = UpdateUser(request.POST, request.FILES, instance=request.user)  # Bind form data
        if form.is_valid():  # Validate the form
            form.save()  # Save the updated user data
            return redirect('profile', request.user.username)  # Redirect to the user's profile

    context = {'form_user': form_user, 'form_password': form_password, 'form_reset_password': form_reset_password}
    return render(request, 'blog/user/update.html', context)

# Function view for logging in a user
def login_user(request):
    if request.method == 'POST':  # Handle form submission
        next_url = request.GET.get('next', 'home')  # Get the next URL or default to 'home'

        email = request.POST['email']  # Get the email from the form
        password = request.POST['password']  # Get the password from the form

        user = get_object_or_404(User, email=email)  # Get the user by email
        if user:
            user = authenticate(request, email=email, password=password)  # Authenticate the user
            login(request, user)  # Log in the user
            return redirect(next_url)  # Redirect to the next URL

    return render(request, 'blog/user/login.html', {})  # Render the login page

# Function view for logging out a user
def logout_user(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the home page

# Function view for rendering the home page
def home(request):
    popular_films = Film.objects.annotate(favorite_count=Count('in_favorites')).order_by('-favorite_count')[:3]  # Get the top 3 popular films
    featured_review = Review.objects.latest("created")  # Get the latest review
    reviews_list = Review.objects.all().order_by('-created')  # Get all reviews ordered by creation date
    paginator = Paginator(reviews_list, 4)  # Paginate reviews (4 per page)
    page = request.GET.get('page', 1)  # Get the current page number
    reviews = paginator.page(page)  # Get the reviews for the current page
    context = {'reviews': reviews, 'featured_review': featured_review, 'popular_films': popular_films}
    return render(request, 'blog/home.html', context)

# Function view for rendering the detail of a review
def review_detail(request, slug):
    review = get_object_or_404(Review, slug=slug)  # Get the review by slug
    comments = Comment.objects.filter(review__id=review.id).order_by('-created')  # Get comments for the review
    related_reviews = Review.objects.filter(film=review.film).exclude(id=review.id)  # Get related reviews
    if request.method == 'POST':  # Handle comment submission
        comment = Comment.objects.create(
            body=request.POST['body'],  # Get the comment body
            user=request.user,  # Set the user
            review=review  # Associate the comment with the review
        )
        comment.save()  # Save the comment
        return redirect('review-detail', slug)  # Redirect to the review detail page

    context = {'review': review, 'comments': comments, 'related_reviews': related_reviews}
    return render(request, 'blog/review/detail.html', context)

# Function view for deleting a comment
def comment_delete(request, id, slug):
    comment = Comment.objects.get(id=id)  # Get the comment by ID
    comment.delete()  # Delete the comment
    return redirect('review-detail', slug)  # Redirect to the review detail page

# Function view for rendering the list of all reviews
def review_list(request):
    popular_films = Film.objects.all()[:3]  # Get the top 3 films
    query_title = request.GET.get('hledat')  # Get the search query

    if query_title:  # If a search query is provided
        review_list = Review.objects.filter(title__icontains=query_title)  # Filter reviews by title
    else:
        review_list = Review.objects.all()  # Get all reviews

    paginator = Paginator(review_list, 6)  # Paginate reviews (6 per page)
    page = request.GET.get('page', 1)  # Get the current page number
    reviews = paginator.page(page)  # Get the reviews for the current page

    context = {'reviews': reviews, 'popular_films': popular_films}
    return render(request, 'blog/review/list.html', context)

# Function view for creating a new review
@login_required
def review_create(request):
    if request.GET.get('film'):  # If a film is provided in the query string
        film = Film.objects.get(slug=request.GET.get('film'))  # Get the film by slug
        form = CreateReview(initial={'film': film})  # Pre-fill the form with the film
    else:
        form = CreateReview()  # Initialize an empty form

    if request.method == 'POST':  # Handle form submission
        form = CreateReview(request.POST, request.FILES)  # Bind form data
        if form.is_valid():  # Validate the form
            review = form.save(commit=False)  # Save the form without committing to the database
            review.author = request.user  # Set the author to the current user
            review.save()  # Save the review
            return redirect('review-list')  # Redirect to the review list

    context = {'form': form}
    return render(request, 'blog/review/create.html', context)

def review_update(request, slug):
    review = Review.objects.get(slug=slug)  # Get the review by slug
    form = CreateReview(instance=review)  # Pre-fill the form with the review's data

    if request.method == 'POST':  # Handle form submission
        form = CreateReview(request.POST, request.FILES, instance=review)  # Bind form data

        if form.is_valid():  # Validate the form
            if not request.FILES.get('image'):  # Check if an image was not uploaded
                form.image = review.image  # Retain the existing image
            form.save()  # Save the updated review
            return redirect('review-list')  # Redirect to the review list

    context = {'form': form}  # Pass the form to the template
    return render(request, 'blog/review/create.html', context)  # Render the review update page

def review_delete(request, slug):
    review = Review.objects.get(slug=slug)  # Get the review by slug

    if request.method == 'POST':  # Handle form submission
        review.delete()  # Delete the review
        return redirect('review-list')  # Redirect to the review list

    context = {'review': review}  # Pass the review to the template
    return render(request, 'blog/review/delete.html', context)  # Render the review delete confirmation page

def film_list(request):
    query_tag = request.GET.get('tag')  # Get the tag filter from the query string
    search_value = request.GET.get('hledat')  # Get the search value from the query string

    if query_tag:  # If a tag is provided
        film_list = Film.objects.filter(tags__slug=query_tag)  # Filter films by the tag
    elif search_value:  # If a search value is provided
        film_list = Film.objects.filter(title__icontains=search_value)  # Filter films by title
    else:
        film_list = Film.objects.all()  # Get all films if no filters are applied

    paginator = Paginator(film_list, 6)  # Paginate films (6 per page)
    page = request.GET.get('page', 1)  # Get the current page number
    films = paginator.page(page)  # Get the films for the current page

    reviews = Review.objects.order_by('-created')[:3]  # Get the 3 most recent reviews
    tags = Tag.objects.annotate(usage_count=Count("taggit_taggeditem_items")).order_by("-usage_count")[0:6]  # Get the top 6 tags by usage
    context = {'films': films, 'reviews': reviews, 'tags': tags}  # Pass the films, reviews, and tags to the template
    return render(request, 'blog/film/list.html', context)  # Render the film list page

def film_detail(request, slug):
    film = Film.objects.get(slug=slug)  # Get the film by slug
    reviews = film.review_set.all()  # Get all reviews associated with the film
    form = AddFilmToFavorites(instance=film)  # Initialize the form for adding the film to favorites
    in_favorites = request.user.favorite_films.filter(film=film).exists()  # Check if the film is in the user's favorites
    try:
        rating = film.review_set.all().aggregate(Avg('rating'))['rating__avg']  # Calculate the average rating of the film
    except TypeError:
        rating = None  # Handle the case where there are no ratings
    context = {
        'film': film,
        'reviews': reviews,
        'rating': rating,
        'form': form,
        'in_favorites': in_favorites
    }  # Pass the film, reviews, rating, form, and favorite status to the template

    return render(request, 'blog/film/detail.html', context)  # Render the film detail page

def film_update(request, slug):
    film = Film.objects.get(slug=slug)  # Get the film by slug
    form = CreateFilm(instance=film)  # Pre-fill the form with the film's data

    if request.method == 'POST':  # Handle form submission
        form = CreateFilm(request.POST, request.FILES, instance=film)  # Bind form data

        if form.is_valid():  # Validate the form
            form.save()  # Save the updated film
            return redirect('film-detail', slug)  # Redirect to the film detail page

    context = {'form': form}  # Pass the form to the template
    return render(request, 'blog/film/create.html', context)  # Render the film update page

def film_delete(request, slug):
    film = Film.objects.get(slug=slug)  # Get the film by slug
    in_favorites = request.user.favorite_films.filter(film=film).exists()  # Check if the film is in the user's favorites
    try:
        rating = film.review_set.all().aggregate(Avg('rating'))['rating__avg']  # Calculate the average rating of the film
    except TypeError:
        rating = None  # Handle the case where there are no ratings

    if request.method == 'POST':  # Handle form submission
        film.delete()  # Delete the film
        return redirect('film-list')  # Redirect to the film list

    context = {'film': film, 'rating': rating, 'in_favorites': in_favorites}  # Pass the film, rating, and favorite status to the template
    return render(request, 'blog/film/delete.html', context)  # Render the film delete confirmation page

def add_favorite_film(request, slug):
    if request.method == 'POST':  # Handle form submission
        film = Film.objects.get(slug=slug)  # Get the film by slug
        favorite_film = FavoriteFilm.objects.create(
            film=film,  # Associate the film
            user=request.user  # Associate the current user
        )
        favorite_film.save()  # Save the favorite film
        return redirect(request.META.get('HTTP_REFERER'))  # Redirect to the previous page

    return redirect(request.META.get('HTTP_REFERER'))  # Redirect to the previous page if not a POST request

def delete_favorite_film(request, slug):
    if request.method == 'POST':  # Handle form submission
        film = Film.objects.get(slug=slug)  # Get the film by slug
        favorite_film = FavoriteFilm.objects.get(user=request.user, film=film)  # Get the favorite film entry
        favorite_film.delete()  # Delete the favorite film entry
        return redirect(request.META.get('HTTP_REFERER'))  # Redirect to the previous page

def film_create(request):
    if request.GET.get('director'):  # Check if a director is provided in the query string
        director = Director.objects.get(slug=request.GET.get('director'))  # Get the director by slug
        form = CreateFilm(initial={'director': director})  # Pre-fill the form with the director
    else:
        form = CreateFilm()  # Initialize an empty form

    if request.method == 'POST':  # Handle form submission
        form = CreateFilm(request.POST, request.FILES)  # Bind form data
        if form.is_valid():  # Validate the form
            form.save()  # Save the new film
            return redirect('film-list')  # Redirect to the film list

    context = {'form': form}  # Pass the form to the template
    return render(request, 'blog/film/create.html', context)  # Render the film creation page

def director_create(request):
    form = CreateDirector()  # Initialize an empty form for creating a director

    if request.method == 'POST':  # Handle form submission
        form = CreateDirector(request.POST, request.FILES)  # Bind form data
        if form.is_valid():  # Validate the form
            form.save()  # Save the new director
            return redirect('film-list')  # Redirect to the film list

    context = {'form': form}  # Pass the form to the template
    return render(request, 'blog/director/create.html', context)  # Render the director creation page

def director_list(request):
    director_list = Director.objects.all().order_by('name')  # Get all directors
    paginator = Paginator(director_list, 20)  # Paginate directors (20 per page)
    page = request.GET.get('page', 1)  # Get the current page number
    directors = paginator.page(page)  # Get the directors for the current page
    popular_films = Film.objects.annotate(favorite_count=Count('in_favorites')).order_by('-favorite_count')[:3]  # Get the top 3 popular films
    reviews = Review.objects.order_by('-created')[:3]  # Get the 3 most recent reviews

    context = {'directors': directors, 'popular_films': popular_films, 'reviews': reviews}  # Pass data to the template
    return render(request, 'blog/director/list.html', context)  # Render the director list page

def director_detail(request, slug):
    director = Director.objects.get(slug=slug)  # Get the director by slug
    directors_films = director.film_set.all()  # Get all films associated with the director
    context = {'director': director, 'directors_films': directors_films}  # Pass the director and their films to the template

    return render(request, 'blog/director/detail.html', context)  # Render the director detail page

def director_update(request, slug):
    director = Director.objects.get(slug=slug)  # Get the director by slug
    form = CreateDirector(instance=director)  # Pre-fill the form with the director's data

    if request.method == 'POST':  # Handle form submission
        form = CreateDirector(request.POST, request.FILES, instance=director)  # Bind form data
        if form.is_valid():  # Validate the form
            form.save()  # Save the updated director
            return redirect('director-detail', slug)  # Redirect to the director detail page

    context = {'form': form}  # Pass the form to the template
    return render(request, 'blog/director/create.html', context)  # Render the director update page

# Function view for deleting a director
def director_delete(request, slug):
    director = Director.objects.get(slug=slug)  # Get the director by slug

    if request.method == 'POST':  # Handle form submission
        director.delete()  # Delete the director
        return redirect('director-list')  # Redirect to the director list

    context = {'director': director}  # Pass the director to the template
    return render(request, 'blog/director/delete.html', context)  # Render the delete confirmation page

# Function view for rendering a user's profile
def profile_user(request, username):
    user = User.objects.get(username=username)  # Get the user by username
    reviews = user.review_set.all()  # Get all reviews written by the user
    form_user = UpdateUser(instance=user)  # Pre-fill the form with the user's data
    form_password = PasswordChangeForm(user)  # Password change form for the user
    favorite_films = user.favorite_films.all()  # Get all films favorited by the user

    # Pass the user, their reviews, the update form, the password change form, and their favorite films to the template
    context = {
        'user': user,
        'reviews': reviews,
        'form_user': form_user,
        'form_password': form_password,
        'favorite_films': favorite_films
    }

    return render(request, 'blog/user/profile.html', context)  # Render the user's profile page

