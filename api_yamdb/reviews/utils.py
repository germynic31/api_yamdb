import random

from . import consts


def generate_confirmation_code(user):
    confirmation_code = random.choices(
        consts.SYMBOLS, k=consts.CONFIRMATION_CODE_LENGTH
    )
    user.confirmation_code = confirmation_code
    user.save()
    return confirmation_code
