from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model
from django.conf import settings

UserModel = get_user_model()


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
    history = HistoricalRecords()
    is_closed = models.BooleanField(default=False)

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


class PageVisit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата посещения')
    url = models.CharField(max_length=2048, verbose_name='URL')
    query_params = models.TextField(verbose_name='GET параметры')
    method = models.CharField(max_length=10, verbose_name='HTTP метод')
    user_agent = models.CharField(max_length=256, verbose_name='User Agent')
    os = models.CharField(max_length=100, verbose_name='Операционная система', blank=True, null=True)
    browser = models.CharField(max_length=100, verbose_name='Браузер', blank=True, null=True)

    class Meta:
        verbose_name = 'Посещение страницы'
        verbose_name_plural = 'Посещения страниц'
