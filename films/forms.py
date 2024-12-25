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
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(PostForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        obj = super(PostForm, self).save(commit=False)
        obj.author = self.author
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Post
        fields = ['name', 'icon']

CreateSectionFormSet = forms.inlineformset_factory(
    Post,
    Section,
    fields=('name', 'body', 'image', 'image_status', 'position'),
    extra=1,
    can_delete=False,
    max_num=None,
)

UpdateSectionFormSet = forms.inlineformset_factory(
    Post,
    Section,
    fields=('name', 'body', 'image', 'image_status', 'position'),
    extra=0,
    can_delete=True,
    max_num=None,
)

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.post = kwargs.pop('post', None)
        super(CommentForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        obj = super(CommentForm, self).save(commit=False)
        obj.author = self.author
        obj.post = self.post
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Напишите комментарий...'}),
        }
        labels = {
            'body': "",
        }