from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db import models

Q = models.Q

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
    middle_name = models.CharField(_("middle name"), blank=True, max_length=50)
    slug = models.SlugField(max_length=150, blank=True)

    class Meta(AbstractUser.Meta):
        # impose a unique constraints for
        # all non blank (empty) slug fields
        constraints = [
            models.UniqueConstraint(
                fields=("slug",), condition=~Q(slug=""), name="unique_user_slug"
            )
        ]

    # Add slug to user instance after saving
    # default slug includes user instance pk
    def save(self, **kwargs):
        super(User, self).save(**kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.first_name} {self.last_name} {self.pk}")
        if not self.username:
            self.username = f"{self.first_name}{self.pk}"

    def __str__(self):
        return f"{self.username}"
