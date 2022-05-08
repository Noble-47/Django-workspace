from django import forms
from django.forms import modelformset_factory


from .models import (
    TestDetail, Quiz,
    Question, Choices
    )

class RegisterForQuizForm(forms.ModelForm):
    class Meta:
        model = TestDetail
        fields = ('quiz', 'candidate',)


class CreateQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = (
            "title",
            "quiz_duration",
            "deadline",
            "pass_mark",
        )


class QuestionForm(forms.ModelForm):

    quiz = forms.TextInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.quiz.widgets.attrs.update({"disable" : True})

    class Meta:
        model = Question
        fields = ("question_text",)
        widget = {
            'question_text' : forms.Textarea(attrs = {
                'placeholder' : "Enter question here"
            }),
        }
        labels = {
            'question_text' : "question : "
        }


class QuestionChoicesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["question"].widgets.attrs.update({"disable" : True})

    class Meta:
        model = Choices
        fields = ("question", "choice", "right")
        labels = {'question_text' : "question : "}
        widgets = {"question" : forms.HiddenInput()}


# class BaseChoiceFormSet(forms.BaseFormSet):
#
#     def is_valid(self, question):
#         """
#         Return True if every form in self.forms is valid.
#
#         Check that quiz is unchanged for each form
#         """
#         if not self.is_bound:
#             return False
#         # Accessing errors triggers a full clean the first time only.
#         self.errors
#         # List comprehension ensures is_valid() is called for all forms.
#         # Forms due to be deleted shouldn't cause the formset to be invalid.
#         # forms with altered quiz field are invalid
#         forms_valid = all([
#             form.is_valid() for form in self.forms
#             if not (self.can_delete and self._should_delete_form(form))
#             and form.fields["quiz"] == quiz
#         ])
#         return forms_valid and not self.non_form_errors()

# ChoiceFormset = modelformset_factory(Choices, form = QuestionChoicesForm, formset = BaseChoiceFormSet, min_num = 1, extra = 1)
ChoiceFormset = modelformset_factory(Choices, form = QuestionChoicesForm, min_num = 1, extra = 4)
# use htmx in handling of form
