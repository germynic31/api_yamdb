from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_username, year_validator
from .consts import (
    NAME_LENGTH, SLUG_LENGTH, USERNAME_LENGTH,
    FIRST_NAME_LENGTH, LAST_NAME_LENGTH,
    EMAIL_LENGTH, ROLE_LENGTH,
    BIO_LENGTH, CONFIRMATION_CODE_LENGTH,
    ADMIN_ROLE, MODER_ROLE
)


class User(AbstractUser):
    class Roles(models.TextChoices):
        user = 'user', 'Пользователь'
        moderator = 'moderator', 'Модератор'
        admin = 'admin', 'Администратор'

    username = models.CharField(
        verbose_name='имя пользователя',
        max_length=USERNAME_LENGTH,
        unique=True,
        validators=(validate_username,)
    )
    first_name = models.CharField(
        'имя',
        max_length=FIRST_NAME_LENGTH,
        blank=True)
    last_name = models.CharField(
        'фамилия',
        max_length=LAST_NAME_LENGTH,
        blank=True)
    email = models.EmailField(
        'адрес электронной почты',
        max_length=EMAIL_LENGTH,
        unique=True,
    )
    role = models.CharField(
        'роль',
        max_length=ROLE_LENGTH,
        choices=Roles.choices,
        default=Roles.user
    )
    bio = models.CharField(
        'биография',
        max_length=BIO_LENGTH,
        blank=True
    )
    confirmation_code = models.CharField(max_length=CONFIRMATION_CODE_LENGTH)

    @property
    def is_admin(self):
        return (
            self.is_superuser or self.role == ADMIN_ROLE
        )

    @property
    def is_moder(self):
        return self.role == MODER_ROLE

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'пользователи'
        default_related_name = 'users'
        ordering = ('username',)


class Genre(models.Model):
    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=SLUG_LENGTH,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=SLUG_LENGTH,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название'
    )
    year = models.IntegerField(
        validators=[year_validator],
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'{self.title}, {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст ревью',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Разрешены значения от 1 до 10'),
            MaxValueValidator(10, 'Разрешены значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:50]
