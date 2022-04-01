from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings

from django_registration.backends.activation.views import (
    RegistrationView as BaseRegistrationView,
)

from .forms import RegistrationForm

# Create your views here.

User = get_user_model()


class RegistrationView(BaseRegistrationView):

    form_class = RegistrationForm
    email_body_template = "django_registration/activation_email_body.html"

    def create_inactive_user(self, form):
        """
        Create the inactive user account and send an email containing
        activation instructions
        """
        new_user = form.save(commit=False)
        # add slug field to new user
        new_user.slug = slugify(new_user.username)
        # set user as inactive
        new_user.is_active = False
        new_user.save()

        self.send_activation_email(new_user)

        return new_user

    def send_activation_email(self, user):
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context["user"] = user
        subject = render_to_string(
            template_name=self.email_subject_template,
            context=context,
            request=self.request,
        )
        # Force subject to a single line to avoid header-injection
        # issues
        subject = "".join(subject.splitlines())
        message = render_to_string(
            template_name=self.email_body_template,
            context=context,
            request=self.request,
        )
        user.email_user(
            subject=subject,
            message=message,
            html_message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
        )


@login_required
def profile_redirect_view(request):
    user = request.user
    profile_url = reverse("profile", kwargs={"profile_slug": user.slug})
    return HttpResponseRedirect(profile_url)


def profile_view(request, profile_slug):
    template_name = "accounts/profile.html"
    user = get_object_or_404(User, slug=profile_slug)
    return render(request, template_name, {"user": user})

    # search for user
    # user = get_object_or_404(User, pk=pk)
    # first_name = None, last_name = None
    # if user.first_name == first_name and user.last_name == last_name:
    #     return render(reqeust, template_name, {"user" : user})
