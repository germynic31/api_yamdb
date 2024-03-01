from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class RoleManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Role(models.Model):
    name = models.CharField(_('name'), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
    )

    objects = RoleManager()

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __str__(self):
        return self.name


class MyUser(AbstractUser):
    email = models.EmailField(
        _('email address'),
        max_length=254,
        blank=True,
        unique=True,
    )
    role = models.ManyToManyField(
        Role,
        verbose_name=_('roles'),
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )
    bio = models.CharField(_('bio'), max_length=256, blank=True)
