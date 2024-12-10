from django.contrib import admin
from .models import Country, Film, Person, Genre, Post, Section, Comment

admin.site.register(Film)
admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Post)
admin.site.register(Section)
admin.site.register(Comment)
