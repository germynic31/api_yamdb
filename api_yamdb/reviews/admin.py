from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import (
    Category, Genre, GenreTitle,
    Title, Review, Comment, User
)


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = (GenreTitleInline,)


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    model = User
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'email',
                    'bio',
                    'first_name',
                    'last_name',
                    'role'
                )
            }
        )
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'bio',
                    'role'
                )
            }
        )
    )


admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
