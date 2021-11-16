from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with unique email."""

    email = models.EmailField(unique=True)
