from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterUser, CreateFilm, CreateDirector, CreateReview, UpdateUser, AddFilmToFavorites
from taggit.models import Tag
from django.db.models import Avg, Count
from django.core.paginator import Paginator
from django.urls import reverse_lazy

def reset_password(request): #function view for reseting user's password utilising django's PasswordResetForm
    form = PasswordResetForm()
    context = {'form':form}
    return render(request, 'blog/user/change_password.html', context)


def register_user(request): #function view for registering the user
    form = RegisterUser()
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'blog/user/register.html', context)

@login_required
def update_user(request): #function view for updating user's information

    form_user = UpdateUser(instance=request.user)
    form_password = PasswordChangeForm(request.user)
    form_reset_password = PasswordResetForm()

    if request.method == 'POST':
        form = UpdateUser(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)
    context = {'form_user':form_user, 'form_password': form_password, 'form_reset_password': form_reset_password}

    return render(request, 'blog/user/update.html', context)

def login_user(request): #function view for logging in the user
    if request.method == 'POST':
        next_url = request.GET.get('next', 'home')

        email = request.POST['email']
        password = request.POST['password']

        user = get_object_or_404(User, email=email)
        if user:
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return redirect(next_url)

    return render(request, 'blog/user/login.html', {})


def logout_user(request): #function view for logging out the user
    logout(request)
    return redirect('home')

def home(request): #function view rendering the home page
    popular_films = Film.objects.all()[:3]
    featured_review = Review.objects.latest("created")
    reviews_list = Review.objects.all()
    paginator = Paginator(reviews_list, 4) #paginating the review to display the maximum of 4 instances on one page
    page = request.GET.get('page', 1)
    reviews = paginator.page(page)
    context = {'reviews': reviews, 'featured_review': featured_review, 'popular_films': popular_films}
    return render(request, 'blog/home.html', context)

def review_detail(request, slug): #function view rendering the detail of a review
    review = get_object_or_404(Review, slug=slug)
    comments = Comment.objects.filter(review__id=review.id).order_by('-created') #comments associated with the review ordered by the creation time from newest to oldest
    related_reviews = Review.objects.filter(film=review.film).exclude(id=review.id)
    if request.method == 'POST':
        comment = (Comment.objects.create
                   (body=request.POST['body'],
                    user=request.user,
                    review=review))
        comment.save()

        return redirect('review-detail', slug)

    context = {'review': review, 'comments': comments, 'related_reviews': related_reviews}
    return render(request, 'blog/review/detail.html', context)

def comment_delete(request, id, slug): #function view for deleting a comment
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect('review-detail', slug)


def review_list(request): #function view rendering the list of all reviews
    popular_films = Film.objects.all()[:3]
    query_title = request.GET.get('hledat')

    if query_title:
        review_list = Review.objects.filter(title__icontains=query_title)
    else:
        review_list = Review.objects.all()

    paginator = Paginator(review_list, 6)
    page = request.GET.get('page', 1)

    reviews = paginator.page(page)

    context = {'reviews': reviews, 'popular_films': popular_films}

    return render(request, 'blog/review/list.html', context)

@login_required
def review_create(request):
    if request.GET.get('film'):
        film = Film.objects.get(slug=request.GET.get('film'))
        form = CreateReview(initial={'film':film})
    else:
        form = CreateReview()
    if request.method == 'POST':
        form = CreateReview(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('review-list')
    context = {'form': form}
    return render(request, 'blog/review/create.html', context)

def review_update(request, slug):
    review = Review.objects.get(slug=slug)
    form = CreateReview(instance=review)

    if request.method == 'POST':
        form = CreateReview(request.POST, request.FILES, instance=review)

        if form.is_valid():
            if not request.FILES.get('image'):
                form.image = review.image
            form.save()
            return redirect('review-list')

    context = {'form': form}
    return render(request, 'blog/review/create.html', context)

def review_delete(request, slug):
    review = Review.objects.get(slug=slug)

    if request.method == 'POST':
        review.delete()
        return redirect('review-list')

    context = {'review': review}
    return render(request, 'blog/review/delete.html', context)



def film_list(request):

    query_tag = request.GET.get('tag')
    search_value = request.GET.get('hledat')

    if query_tag:
        film_list = Film.objects.filter(tags__slug=query_tag)
        print(query_tag)
    elif search_value:
        film_list = Film.objects.filter(title__icontains=search_value)
    else:
        film_list = Film.objects.all()

    paginator = Paginator(film_list, 6)
    page = request.GET.get('page', 1)
    films = paginator.page(page)

    reviews = Review.objects.order_by('-created')[:3]
    tags = Tag.objects.annotate(usage_count=Count("taggit_taggeditem_items")).order_by("-usage_count")[0:6]
    context = {'films': films, 'reviews': reviews, 'tags': tags}
    return render(request, 'blog/film/list.html', context)

def film_detail(request, slug):
    film = Film.objects.get(slug=slug)
    reviews = film.review_set.all()
    form = AddFilmToFavorites(instance=film)
    in_favorites = request.user.favorite_films.filter(film=film).exists()
    try:
        rating = film.review_set.all().aggregate(Avg('rating'))['rating__avg']
    except TypeError:
        rating = None
    context = {'film': film, 'reviews': reviews, 'rating':rating, 'form':form, 'in_favorites': in_favorites}

    return render(request, 'blog/film/detail.html', context)

def add_favorite_film(request, slug):
    if request.method == 'POST':
        film = Film.objects.get(slug=slug)
        favorite_film = (FavoriteFilm.objects.create(
            film=film,
            user=request.user
            ))
        favorite_film.save()
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

def delete_favorite_film(request, slug):
    if request.method == 'POST':
        film = Film.objects.get(slug=slug)
        favorite_film = FavoriteFilm.objects.get(user=request.user, film=film)
        favorite_film.delete()
        return redirect(request.META.get('HTTP_REFERER'))



def film_create(request):
    form = CreateFilm()

    if request.method == 'POST':
        form = CreateFilm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('film-list')
    context = {'form': form}

    return render(request, 'blog/film/create.html', context)

def director_create(request):
    form = CreateDirector()

    if request.method == 'POST':
        form = CreateDirector(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('film-list')

    context = {'form': form}
    return render(request, 'blog/director/create.html', context)

def profile_user(request, username):
    user = User.objects.get(username=username)
    reviews = user.review_set.all()
    form_user = UpdateUser(instance=user)
    form_password = PasswordChangeForm(user)
    favorite_films = user.favorite_films.all()

    context = {'user': user, 'reviews': reviews, 'form_user': form_user, 'form_password': form_password, 'favorite_films': favorite_films}

    return render(request, 'blog/user/profile.html', context)

