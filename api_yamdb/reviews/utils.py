import random


def generate_confirmation_code(user):
    confirmation_code = random.randint(111111, 999999)
    user.confirmation_code = confirmation_code
    user.save()
    return confirmation_code
