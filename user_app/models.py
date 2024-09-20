from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class App_user(AbstractUser):
    email = models.EmailField(
        unique=True, validators=[validators.EmailValidator(message="Invalid Email")]
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
