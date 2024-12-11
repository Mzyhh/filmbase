from django.contrib import admin
from .models import Country, Film, Person, Genre, Post, Section, Comment

admin.site.register(Film)
admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Section)
admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'
    ordering = ['created_at']
    show_facets = admin.ShowFacets.ALWAYS