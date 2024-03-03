from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

ROLES = [
        ('Пользователь', 'user'),
        ('Модератор', 'moder'),
        ('Админ', 'admin'),
        ('Суперюзер', 'superuser')
]


class MyUser(AbstractUser):
    email = models.EmailField(
        _('адрес электронной почты'),
        max_length=254,
        blank=True,
        unique=True,
    )
    role = models.CharField(
        _('role'),
        max_length=28,
        choices=ROLES,
        default='user'
    )
    bio = models.CharField(_('bio'), max_length=256, blank=True)
    confirmation_code = models.CharField(max_length=6)
