import re

from django.core.exceptions import ValidationError

pattern = r'[\w.@+-]'


def validate_username(username):
    if username == 'me':
        raise ValidationError(
            f'Имя пользователя {username} запрещено.'
        )
    x = re.sub(pattern, '', username)
    if x:
        x = ''.join(set(x))
        raise ValidationError(
            f'Нельзя использовать символы: {x}'
        )

    return username
