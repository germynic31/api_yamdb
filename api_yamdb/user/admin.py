from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import MyUser


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    model = MyUser
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
