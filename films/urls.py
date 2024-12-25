from django.urls import path
from . import views

app_name = "films"
urlpatterns = [
     path('', views.film_list, name='home'),
     path('countries/', views.country_list, name='country_list'),
     path('countries/<int:id>/', views.country_detail, name='country_detail'),
     path('countries/create/', views.country_create, name='country_create'),
     path('countries/<int:id>/update/',
          views.country_update, name='country_update'),
     path('countries/<int:id>/delete/',
          views.country_delete, name='country_delete'),
     path('countries/autocomplete/',
          views.CountryAutocomplete.as_view(), name='country_autocomplete'),

     path('genres/', views.genre_list, name='genre_list'),
     path('genres/<int:id>/', views.genre_detail, name='genre_detail'),
     path('genres/create/', views.genre_create, name='genre_create'),
     path('genres/<int:id>/update/',
          views.genre_update, name='genre_update'),
     path('genres/<int:id>/delete/',
          views.genre_delete, name='genre_delete'),

     path('films/', views.film_list, name='film_list'),
     path('films/<int:id>/', views.film_detail, name='film_detail'),
     path('films/create/', views.film_create, name='film_create'),
     path('films/<int:id>/update/',
          views.film_update, name='film_update'),
     path('film/<int:id>/delete/',
          views.film_delete, name='film_delete'),

     path('people/', views.person_list, name='person_list'),
     path('people/<int:id>/', views.person_detail, name='person_detail'),
     path('people/create/', views.person_create, name='person_create'),
     path('people/<int:id>/update/',
          views.person_update, name='person_update'),
     path('people/<int:id>/delete/',
          views.person_delete, name='person_delete'),
     path('people/autocomplete/',
          views.PersonAutocomplete.as_view(), name='person_autocomplete'),

     path('posts/', views.post_list, name='post_list'),
     path('posts/<int:id>/', views.post_detail, name='post_detail'),
     path('posts/<int:id>/update/',
          views.post_update, name='post_update'),
     path('posts/<int:id>/delete/',
          views.post_delete, name='post_delete'),
     path('post/create/', views.post_create, name='post_create'),
     path('comment/<int:id>/delete/', views.comment_delete, name='comment_delete')
]
