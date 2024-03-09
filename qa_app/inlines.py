from django.contrib import admin
from .models import Answer


class AnswerInline(admin.TabularInline):
	model = Answer
	extra = 1
