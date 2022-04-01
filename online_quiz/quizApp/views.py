from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse

from .forms import CreateQuizForm, ChoiceFormset
from .models import Quiz
# Create your views here.


def home(request):
    # add pagination
    # List all ongoing quiz
    queryset = Quiz.objects.filter(status="ONGN")
    template_name = "quizApp/home.html"
    context = {"ongoing_quiz": queryset}
    return render(request, template_name, context)

def setup_view(request):
    pass

class CreateQuizView(CreateView):
    template_name = "quizApp/create_quiz_form.html"
    form_class = CreateQuizForm
    object = None

    def form_valid(self, form):
        """
        Setup other required attributes of Quiz
        model instance
        """
        quiz = form.save(commit = False)
        quiz.quiz_master = self.request.user
        quiz.status = Quiz.QuizStatus.ONGOING
        quiz.save()
        self.object = quiz
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        Redirect user to fill in questions
        and choices for newly created quiz
        access user with self.request.user
        """
        obj = self.object
        url = reverse("setup_quiz", kwargs = {'pk' : obj.pk, 'title' : obj.title})
        return str(url)

    @method_decorator(login_required, name = 'dispatch')
    def dispatch(self, request, *args, **kwargs):
        """
        Ensure only authenticated users has access
        using the login_required decorator
        """
        return super().dispatch(request, *args, **kwargs)
