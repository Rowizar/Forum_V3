from django.contrib import admin
from .models import Category, UserCategoryPreference, Question, QuestionRating, Answer, AnswerRating, Bookmark

# Register your models here.

admin.site.register(Category)
admin.site.register(UserCategoryPreference)
admin.site.register(Question)
admin.site.register(QuestionRating)
admin.site.register(Answer)
admin.site.register(AnswerRating)
admin.site.register(Bookmark)