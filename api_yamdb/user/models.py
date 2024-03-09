from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class MyUser(AbstractUser):
    class Roles(models.TextChoices):
        user = 'user', 'Пользователь'
        moderator = 'moderator', 'Модератор'
        admin = 'admin', 'Администратор'

    username = models.CharField(
        verbose_name='имя пользователя',
        max_length=150,
        unique=True,
        validators=(validate_username,)
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True)
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True)
    email = models.EmailField(
        'адрес электронной почты',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        'роль',
        max_length=max(len(choise) for choise in list(Roles)),
        choices=Roles.choices,
        default=Roles.user
    )
    bio = models.CharField(
        'биография',
        max_length=256,
        blank=True
    )
    confirmation_code = models.CharField(max_length=6)

    @property
    def is_admin(self):
        return (
            self.is_superuser or self.is_staff
            or self.role == 'admin'
        )

    @property
    def is_moder(self):
        return self.role == 'moder'

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'пользователи'
        default_related_name = 'users'
        ordering = ('username',)
