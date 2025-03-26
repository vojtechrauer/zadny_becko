from django.urls import path, reverse_lazy, include
from django.contrib.auth.views import PasswordChangeView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include('api.urls')),
    path('recenze/', views.review_list, name='review-list'),
    path('recenze/<slug:slug>', views.review_detail, name='review-detail'),
    path('recenze/<slug:slug>/smazat-komentar/<int:id>', views.comment_delete, name='comment-delete'),
    path('prihlaseni/', views.login_user, name='login'),
    path('odhlaseni/', views.logout_user, name='logout'),
    path('registrace/', views.register_user, name='register'),
    path('filmy/', views.film_list, name='film-list'),
    path('filmy/<slug:slug>', views.film_detail, name='film-detail'),
    path('smazat-film/<slug:slug>', views.film_delete, name='film-delete'),
    path('upravit-film/<slug:slug>', views.film_update, name='film-update'),
    path('filmy/<slug:slug>/oblibene/pridat', views.add_favorite_film, name='add-favorite-film'),
    path('filmy/<slug:slug>/oblibene/odebrat', views.delete_favorite_film, name='delete-favorite-film'),
    path('pridat-film/', views.film_create, name='film-create'),
    path('reziseri/list', views.director_list, name='director-list'),
    path('reziseri/<slug:slug>', views.director_detail, name='director-detail'),
    path('pridat-rezisera/', views.director_create, name='director-create'),
    path('upravit-rezisera/<slug:slug>', views.director_update, name='director-update'),
    path('smazat-rezisera/<slug:slug>', views.director_delete, name='director-delete'),
    path('pridat-recenzi/', views.review_create, name='review-create'),
    path('upravit-recenzi/<slug:slug>', views.review_update, name='review-update'),
    path('smazat-recenzi/<slug:slug>', views.review_delete, name='review-delete'),
    path('profil/<slug:username>', views.profile_user, name='profile'),
    path('profil/heslo/zmenit', PasswordChangeView.as_view(success_url=reverse_lazy('home')), name='password-change'),
    path('profil/upravit/', views.update_user, name='user-update')
]
