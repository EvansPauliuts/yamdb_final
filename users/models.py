from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class Role(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer. '
                   'Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': "A user with that username already exists.",
        },
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField('email address', unique=True)

    def __str__(self):
        return f'{self.email}'

    @property
    def is_user(self):
        return self.role == Role.USER or self.is_admin or self.is_moderator

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR or self.is_admin

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_staff is True
