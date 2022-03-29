from django.shortcuts import render


from .models import Quiz
# Create your views here.

def home(request):
    # add pagination
    # List all ongoing quiz
    queryset = Quiz.objects.filter(status = "ONGN")
    template_name = "quiz/home.html"
    context = {'ongoing_quiz' : queryset}
    return render(template_name, context)


# def take_quiz(request, pk):
#     pass
