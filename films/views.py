from dal import autocomplete
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from .models import Country, Film, Genre, Person, Post, Section
from .forms import CountryForm, GenreForm, FilmForm, PersonForm, PostForm, CreateSectionFormSet, UpdateSectionFormSet
from .helpers import paginate
from django.contrib import messages

def check_admin(user):
    return user.is_superuser

def check_authenticity(user):
    return user.is_authenticated


def country_list(request):
    countries = Country.objects.all()
    return render(request, 'films/country/list.html', {'countries': countries})


def country_detail(request, id):
    country = get_object_or_404(Country, id=id)
    films = Film.objects.filter(country=country)

    films = paginate(request, films)
    return render(request, 'films/country/detail.html',
                  {'country': country, 'films': films})


@user_passes_test(check_admin)
def country_create(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            country = form.save()
            messages.success(request, 'Страна добавлена')
            return redirect('films:country_detail', id=country.id)
    else:
        form = CountryForm()
    return render(request, 'films/country/create.html', {'form': form})


@user_passes_test(check_admin)
def country_update(request, id):
    country = get_object_or_404(Country, id=id)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            messages.success(request, 'Страна изменена')
            return redirect('films:country_detail', id=country.id)
    else:
        form = CountryForm(instance=country)
    return render(request, 'films/country/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def country_delete(request, id):
    country = get_object_or_404(Country, id=id)
    if request.method == 'POST':
        country.delete()
        messages.success(request, 'Страна удалена')
        return redirect('films:country_list')
    return render(request, 'films/country/delete.html',
                  {'country': country})


def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'films/genre/list.html', {'genres': genres})


def genre_detail(request, id):
    genre = get_object_or_404(Genre, id=id)
    films = Film.objects.filter(genres=genre)

    films = paginate(request, films)
    return render(request, 'films/genre/detail.html',
                  {'genre': genre, 'films': films})


@user_passes_test(check_admin)
def genre_create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save()
            messages.success(request, 'Жанр добавлен')
            return redirect('films:genre_detail', id=genre.id)
    else:
        form = GenreForm()
    return render(request, 'films/genre/create.html', {'form': form})


@user_passes_test(check_admin)
def genre_update(request, id):
    genre = get_object_or_404(Genre, id=id)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Жанр изменён')
            return redirect('films:genre_detail', id=genre.id)
    else:
        form = GenreForm(instance=genre)
    return render(request, 'films/genre/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def genre_delete(request, id):
    genre = get_object_or_404(Genre, id=id)
    if request.method == 'POST':
        genre.delete()
        messages.success(request, 'Жанр удалён')
        return redirect('films:genre_list')
    return render(request, 'films/genre/delete.html',
                  {'genre': genre})


def film_list(request):
    films = Film.objects.all()
    query = request.GET.get('query', '')
    if query:
        films = films.filter(name__icontains=query)
    films = paginate(request, films)
    return render(request, 'films/film/list.html', {'films': films,
                                                    'query': query})


def film_detail(request, id):
    queryset = Film.objects.prefetch_related("country", "genres", "director",
                                             "people")
    film = get_object_or_404(queryset, id=id)
    return render(request, 'films/film/detail.html',
                  {'film': film})


@user_passes_test(check_admin)
def film_create(request):
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            film = form.save()
            messages.success(request, 'Фильм добавлен')
            return redirect('films:film_detail', id=film.id)
    else:
        form = FilmForm()
    return render(request, 'films/film/create.html', {'form': form})


@user_passes_test(check_admin)
def film_update(request, id):
    film = get_object_or_404(Film, id=id)
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES, instance=film)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фильм изменён')
            return redirect('films:film_detail', id=film.id)
    else:
        form = FilmForm(instance=film)
    return render(request, 'films/film/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def film_delete(request, id):
    film = get_object_or_404(Film, id=id)
    if request.method == 'POST':
        film.delete()
        messages.success(request, 'Фильм удалён')
        return redirect('films:film_list')
    return render(request, 'films/film/delete.html',
                  {'film': film})


def person_list(request):
    people = Person.objects.all()
    query = request.GET.get('query', '')
    if query:
        people = people.filter(name__icontains=query)
    people = paginate(request, people)
    return render(request, 'films/person/list.html', {'people': people,
                                                      'query': query})


def person_detail(request, id):
    queryset = Person.objects.prefetch_related("film_set", "directed_films")
    person = get_object_or_404(queryset, id=id)
    return render(request, 'films/person/detail.html',
                  {'person': person})


@user_passes_test(check_admin)
def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save()
            messages.success(request, 'Персона добавлена')
            return redirect('films:person_detail', id=person.id)
    else:
        form = PersonForm()
    return render(request, 'films/person/create.html', {'form': form})


@user_passes_test(check_admin)
def person_update(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Персона изменена')
            return redirect('films:person_detail', id=person.id)
    else:
        form = PersonForm(instance=person)
    return render(request, 'films/person/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def person_delete(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        person.delete()
        messages.success(request, 'Персона удалена')
        return redirect('films:person_list')
    return render(request, 'films/person/delete.html',
                  {'person': person})

def post_list(request):
    posts = Post.objects.all()
    query = request.GET.get('query', '')
    if query:
        posts = posts.filter(name__icontains=query)
    posts = paginate(request, posts)
    return render(request, 'films/post/list.html', {'posts': posts,
                                                      'query': query})

def post_detail(request, id):
    queryset = Post.objects.all()
    post = get_object_or_404(queryset, id=id)
    return render(request, 'films/post/detail.html',
                  {'post': post})

@user_passes_test(check_authenticity)
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        messages.warning(request, 'Вы не можете редактировать пост чужого авторства')
        return redirect('films:post_detail', id=post.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post, author=post.author)
        formset = UpdateSectionFormSet(request.POST, request.FILES, instance=post)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Новость изменена')
            return redirect('films:post_detail', id=post.id)
    else:
        form = PostForm(instance=post, author=post.author)
        formset = UpdateSectionFormSet(instance=post)
    return render(request, 'films/post/update.html', 
                  {'form': form, 'formset' : formset})

@user_passes_test(check_authenticity)
def post_create(request):
    if request.method == 'POST':
        form = PostForm(author=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save()
            formset = CreateSectionFormSet(request.POST, request.FILES, instance=post)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Новость добавлена')
                return redirect('films:post_detail', id=post.id)
    else:
        form = PostForm()
        formset = CreateSectionFormSet()
    return render(request, 'films/post/create.html', 
                  {'form': form, 'formset' : formset})

@user_passes_test(check_authenticity)
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        messages.warning(request, 'Вы не можете удалить пост чужого авторства')
        return redirect('films:post_detail', id=post.id)
    if request.method == 'POST':
        for section in post.sections.all():
            section.delete()
        post.delete()
        messages.success(request, 'Пост удалён')
        return redirect('films:post_list')
    return render(request, 'films/post/delete.html',
                 {'post': post})

class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        people = Person.objects.all()
        if self.q:
            people = people.filter(name__istartswith=self.q)
        return people


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        countries = Country.objects.all()
        if self.q:
            countries = countries.filter(name__istartswith=self.q)
        return countries
