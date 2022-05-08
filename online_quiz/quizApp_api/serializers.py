from quizApp.models import (Quiz,)

from rest_framework import serializers

class QuizSerializer(serializers.ModelSerialiizer):
    class Meta:
        model = Quiz
        fields = ["title", "quiz_master", "created", "deadline", "status", "quiz_duration", "candidate", "pass_mark"]
        extra_kwargs = {
            "candidates" : {"read_only" : True}, 
            "created" : {"read_only" : True}
            "status" : {"read_only" : True}
            }

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["quiz", "question_text"]
        extra_kwargs = {"quiz" : {"read_only" : True}}


class ChioceSerializer(serializers.ModelSerialiizer):
    class Meta:
        model = Choices
        fields = ["question", "choice"]
        extra_kwargs = {"question" : {"read_only" : True}}        


class TestDetailSerializer(serializers.ModelSerialiizer):
    class Meta:
        model = TestDetail
        fields = ["candidate", "quiz", "score", "start_time", "end_time", "quiz_status"]
        extra_kwargs = {
            "score" : {"read_only" : True},
            "start_time" : {"read_only" : True},
            "end_time" : {"read_only" : True},
            "quiz_status" : {"read_only" : True}
        }