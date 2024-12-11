from django import forms
from dal import autocomplete
from .models import Country, Genre, Film, Person, Post, Comment, Section


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['name', 'origin_name', 'slogan', 'length', 'year',
                  'trailer_url', 'cover', 'description', 'country', 'genres',
                  "director", 'people']
        widgets = {
            'people': autocomplete.ModelSelect2Multiple(
                url='films:person_autocomplete'),
            'director': autocomplete.ModelSelect2(
                url='films:person_autocomplete'),
            'country': autocomplete.ModelSelect2(
                url='films:country_autocomplete'),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'origin_name', 'birthday', 'photo']
        widgets = {
            "birthday": forms.DateInput(attrs={'type': 'date'},
                                        format="%Y-%m-%d")
        }

class PostForm(forms.ModelForm):
    def __init__(self, **kwargs):
        self.author = kwargs.pop('author', None)
        super(PostForm, self).__init__(**kwargs)
    
    def save(self, commit=True):
        obj = super(PostForm, self).save(commit=False)
        obj.author = self.author
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Post
        fields = ['name', 'icon']