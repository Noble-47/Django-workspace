from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.

User = get_user_model()


class Quiz(models.Model):

    class QuizStatus(models.TextChoices):
        ONGOIN = "ONGN", _("ongoing")
        SUSPENDED = "SPND", _("suspended")
        CONCLUDED = "CNLD", _("concluded")

    subject = models.CharField(max_length=100)
    quiz_master = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    conducted = models.BooleanField(default=False)
    date = models.DateTimeField()
    status = models.CharField(max_length = 4, choices = QuizStatus.choices)
    def __str__(self):
        return f"{self.quiz_master} : {self.subject}--{self.date}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return f"{self.quiz} : {self.question_text}"


class Choices(models.Model):
    choice = models.TextField()
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    right = models.BooleanField(default=False)

    def __str__(self):
        return f"choices to {self.question.id}"
