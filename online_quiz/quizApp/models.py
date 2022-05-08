from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class TestDetail(models.Model):
    class TestStatus(models.TextChoices):
        ONGOING = "ONGN", _("ongoing")
        CONCLUDED = "CNLD", _("concluded")
        PENDING = "PNDG", _("pending")  # registered but yet to take

    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)
    score = models.PositiveIntegerField(blank=True)

    # allow user to register without taking test
    test_status = models.CharField(
        max_length=4, choices=TestStatus.choices, default=TestStatus.PENDING
    )

    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)

    class Meta:
        # add unique constraint for test_taker and quiz
        ordering = ["-score"]
        constraints = [
            # A candidate can register and take
            # a quiz only once
            models.UniqueConstraint(
                fields=["quiz", "candidate"], name="Unique_test_for_quiz_and_candidate"
            )
        ]

    def __str__(self):
        return f"{self.candidate} : {self.quiz}"


class Quiz(models.Model):
    class QuizStatus(models.TextChoices):
        ONGOING = "ONGN", _("ongoing")
        SUSPENDED = "SPND", _("suspended")
        CONCLUDED = "CNLD", _("concluded")

    title = models.CharField(max_length=100)
    quiz_master = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz")
    candidate = models.ManyToManyField(User, through=TestDetail, related_name="tests")
    quiz_duration = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=4, choices=QuizStatus.choices, default=QuizStatus.ONGOING
    )
    pass_mark = models.PositiveIntegerField()  # in percentage

    def get_top(self):
        if self.status == "SPND":
            return None
        return self.candidate.all()

    def __str__(self):
        return f"{self.quiz_master} : {self.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return f"{self.quiz.title} : {self.question_text}"


class Choices(models.Model):
    choice = models.TextField()
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    right = models.BooleanField(default=False)

    def __str__(self):
        return f"choices to {self.question.id}"
