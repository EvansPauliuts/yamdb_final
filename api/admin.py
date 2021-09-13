from django.contrib import admin

from .models import Categories, Comment, Genres, GenreTitle, Review, Titles

admin.site.register(Genres)
admin.site.register(GenreTitle)
admin.site.register(Categories)
admin.site.register(Titles)
admin.site.register(Review)
admin.site.register(Comment)
