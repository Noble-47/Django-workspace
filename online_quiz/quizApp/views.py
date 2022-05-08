from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import CreateQuizForm, ChoiceFormset, QuestionForm
from .models import Quiz, Question
# Create your views here.

def setup_question_view(request, title, pk):
    template_name = "quizApp/question_form.html"
    quiz = get_object_or_404(Quiz, pk = pk)
    form = QuestionForm({"quiz" : quiz})
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            # ensure that quiz field was unaltered
            if form.fields["quiz"] == quiz:
                form.save()
    return render(request, template_name = template_name, context = {"form" : form})

def add_choices_view(request, question_text, pk):
    """
    Handles next step in creating a quiz
    this include setting the Quiz question
    and their actual choices

    pk : primary key of Question instance
    """
    template_name = "quizApp/choices_form.html"
    question = get_object_or_404(Question, pk = pk)
    formset = ChoiceFormset()
    if request.method == "POST":
        formset = ChoiceFormset(request.POST)
        if formset.is_valid():
            # ensure that pk is not changed
            for form in formset.forms:
                if form.fields["question"] == question:
                    form.save()
    return render(request, template_name = template_name, context = {"formset" : formset})


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


class HomeView(ListView):

    queryset = Quiz.objects.filter(status="ONGN")
    model = Quiz
    template_name = "quizApp/home.html"
    context = {"ongoing_quiz": queryset}

    def get_context_data(self, *args, **kwargs):
        ctx = super(HomeView, self).get_context_data(*args, **kwargs)
        ctx.update(self.context)
        return ctx
