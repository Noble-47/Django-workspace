from django.contrib.auth import get_user_model
from django.shortcuts import render

from quizApp.models import Quiz


def home_view(request):
    # Shows all ongoing and concluded quiz
    # add pagination
    quiz_list = Quiz.objects.exclude(status="SPND")
    ongoing = [quiz for quiz in quiz_list if quiz.status == "ONGN"]
    concluded = [quiz for quiz in quiz_list if quiz.status == "CNLD"]
    context = {
        "ongoing": ongoing,
        "concluded": concluded,
    }

    return render(request, "/online_quiz/home.html", context=context)
