from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.

User = get_user_model()


class TestDetail(models.Model):
    test_taker = models.ForeignKey(User, on_delete = models.CASCADE)
    quiz = models.ForeignKey("Quiz", on_delete = models.CASCADE)
    start_time = models.DateTimeField(auto_now_add = True)
    end_time = models.DateTimeField()
    score = models.PositiveIntegerField()

    class Meta:
        ordering = ["-score"]

    def __str__(self):
        return f"{self.quiz} : {self.test_taker}"


class Quiz(models.Model):

    class QuizStatus(models.TextChoices):
        ONGOIN = "ONGN", _("ongoing")
        SUSPENDED = "SPND", _("suspended")
        CONCLUDED = "CNLD", _("concluded")

    subject = models.CharField(max_length=100)
    quiz_master = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "quiz")
    candidate = models.ManyToManyField(User, through = TestDetail, related_name = 'tests')
    quiz_duration = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add = True)
    deadline = models.DateTimeField()
    status = models.CharField(max_length = 4, choices = QuizStatus.choices)
    pass_mark = models.PositiveIntegerField() # in percentage

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
