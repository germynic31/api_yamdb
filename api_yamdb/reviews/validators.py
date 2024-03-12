import re

from django.core.exceptions import ValidationError
from django.utils import timezone

pattern = r'[\w.@+-]'


def year_validator(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            'Год выпуска произведения не может быть больше текущего'
        )


def validate_username(username):
    if username == 'me':
        raise ValidationError(
            f'Имя пользователя {username} запрещено.'
        )
    forbidden_symbols = re.sub(pattern, '', username)
    if forbidden_symbols:
        forbidden_symbols = ''.join(set(forbidden_symbols))
        raise ValidationError(
            f'Нельзя использовать символы: {forbidden_symbols}'
        )

    return username
