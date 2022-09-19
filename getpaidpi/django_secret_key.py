"""
Generate a `SECRET_KEY` value for a new Django project/environment.
"""

from django.core.management.utils import get_random_secret_key
from django.utils.crypto import get_random_string
import hashlib


def key_generator(length=70):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    key = get_random_string(length=length, allowed_chars=chars)

    return key


if __name__ == '__main__':
    key_generator()