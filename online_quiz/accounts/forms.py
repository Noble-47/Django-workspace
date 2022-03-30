from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from django_registration.forms import RegistrationFormUniqueEmail
from django_registration import validators

User = get_user_model()


class QuizRegistrationForm(RegistrationFormUniqueEmail):
    def __init__(self, *args, **kwargs):
        super(QuizRegistrationForm, self).__init__(*args, **kwargs)
        # applys a case insensitive unique validator to username field
        self.fields[User.USERNAME_FIELD].validators.append(
            validators.CaseInsensitiveUnique(
                User, User.USERNAME_FIELD, validators.DUPLICATE_USERNAME
            )
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name"] + RegistrationFormUniqueEmail.Meta.fields
