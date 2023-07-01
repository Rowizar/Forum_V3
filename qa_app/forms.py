from django import forms
from .models import Question
from .models import Answer


class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'text', 'image']


class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['text']
