from django.urls import path

from .views import home, CreateQuizView, setup_view

app_name = "quizApp"

urlpatterns = [
    path('', home, name = "home"),
    path('create-quiz/', CreateQuizView.as_view(), name = "create_quiz"),
    path('setup-quiz/<str:title>/<int:pk>/', setup_view, name = "setup_quiz"),
]
