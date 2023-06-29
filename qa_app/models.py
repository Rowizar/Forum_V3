from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()


class Question(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	text = models.TextField()
	pub_date = models.DateTimeField('date published')


class Answer(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.TextField()
	pub_date = models.DateTimeField('date published')


class QuestionRating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	rating = models.IntegerField()


class AnswerRating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
	rating = models.IntegerField()


class UserCategoryPreference(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	preference_level = models.IntegerField()
