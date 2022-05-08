from django.contrib import admin
from quizApp.models import Quiz
# Register your models here.

class QuizAppAdmin(admin.ModelAdmin):
	model = Quiz

admin.site.register(Quiz, QuizAppAdmin)
