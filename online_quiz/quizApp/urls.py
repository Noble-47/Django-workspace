from django.urls import path

from . import views
from .views import HomeView, CreateQuizView

app_name = "quizApp"

urlpatterns = [
    path('', HomeView.as_view(), name = "home"),
    path('create-quiz/', CreateQuizView.as_view(), name = "create_quiz"),
    path('setup-quiz/<str:title>/<int:pk>/', views.setup_question_view, name = "add_question"),
    path('question/<str:question_text>/<int:pk>/', views.add_choices_view, name = "add_choices"),
]
