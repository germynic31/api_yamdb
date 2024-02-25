from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):
    email = models.EmailField(
        _('email address'),
        max_length=254,
        blank=True,
        unique=True,
    )
    bio = models.CharField(_('bio'), max_length=256, blank=True)
    role = models.CharField(_('role'), max_length=128, default='user')
