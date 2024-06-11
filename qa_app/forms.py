from django import forms
from .models import Question
from .models import Answer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'text', 'image']


class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['text']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
