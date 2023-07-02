from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()

	def __str__(self):
		return self.name


class Question(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	title = models.CharField(max_length=200, default=None)
	text = models.TextField()
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	pub_date = models.DateTimeField(auto_now_add=True)
	categories = models.ManyToManyField(Category, blank=True)

	def get_rating(self):
		ratings = QuestionRating.objects.filter(question=self)
		return sum(rating.rating for rating in ratings)

	def __str__(self):
		return self.title


class Answer(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.TextField()
	pub_date = models.DateTimeField(auto_now_add=True)

	def get_rating(self):
		ratings = AnswerRating.objects.filter(answer=self)
		return sum(rating.rating for rating in ratings)

	def __str__(self):
		return self.text


class QuestionRating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	rating = models.IntegerField()

	def __str__(self):
		return str(self.rating)


class AnswerRating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
	rating = models.IntegerField()

	def __str__(self):
		return str(self.rating)


class UserCategoryPreference(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	preference_level = models.IntegerField()

	def __str__(self):
		return str(self.user) + str(self.category)


class Bookmark(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = (
			'user',
			'question')  # чтобы предотвратить повторные закладки одного и того же вопроса одним пользователем

	def __str__(self):
		return f'{self.user.username} bookmarked {self.question.title}'
