from django.contrib import admin
from reviews.models import Category, Genre, GenreTitle, Title


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = (GenreTitleInline,)


admin.site.register(Genre)
admin.site.register(Category)
