from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            'Год выпуска произведения не может быть больше текущего'
        )
