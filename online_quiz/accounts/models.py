from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
        # validators=[username_validator],
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return f"{self.username}"
