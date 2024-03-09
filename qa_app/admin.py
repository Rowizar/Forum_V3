from django.contrib import admin
from django.template.defaultfilters import truncatechars
from simple_history.admin import SimpleHistoryAdmin
from .models import Category, UserCategoryPreference, Question, QuestionRating, Answer, AnswerRating, Bookmark


# Register your models here.
class QuestionAdmin(SimpleHistoryAdmin):
	list_display = ('title_short', 'author', 'pub_date', 'get_rating')


class AnswerInline(admin.TabularInline):  # или admin.StackedInline
	model = Answer
	extra = 1  # Количество пустых форм по умолчанию


class QuestionAdmin(admin.ModelAdmin):
	list_display = ('title_short', 'author', 'pub_date', 'get_rating')
	list_filter = ('author', 'pub_date', 'categories')
	search_fields = ('title', 'author__username')
	date_hierarchy = 'pub_date'
	inlines = [AnswerInline, ]
	readonly_fields = ('get_rating',)
	filter_horizontal = ('categories',)

	def get_rating(self, obj):
		return obj.get_rating()

	def title_short(self, obj):
		return truncatechars(obj.title, 10)

	title_short.short_description = 'Title'
	get_rating.short_description = 'Rating'


class AnswerAdmin(admin.ModelAdmin):
	list_display = ('text_short', 'question_short', 'user', 'pub_date', 'get_rating')
	list_filter = ('user', 'pub_date')
	search_fields = ('question__title', 'user__username', 'text')
	raw_id_fields = ('question',)

	def get_rating(self, obj):
		return obj.get_rating()

	def text_short(self, obj):
		return truncatechars(obj.text, 10)

	def question_short(self, obj):
		return truncatechars(obj.question.title, 10)

	text_short.short_description = 'Text'
	get_rating.short_description = 'Rating'


class QuestionRatingAdmin(admin.ModelAdmin):
	list_display = ('question_short', 'user', 'rating')
	list_filter = ('user', 'rating')
	raw_id_fields = ('question',)

	def question_short(self, obj):
		return truncatechars(obj.question.title, 10)


class AnswerRatingAdmin(admin.ModelAdmin):
	list_display = ('answer_short', 'user', 'rating')
	list_filter = ('user', 'rating')
	raw_id_fields = ('answer',)

	def answer_short(self, obj):
		return truncatechars(obj.answer.text, 10)


class BookmarkAdmin(admin.ModelAdmin):
	list_display = ('user', 'question_short', 'created_at')
	list_filter = ('user', 'created_at')
	raw_id_fields = ('question',)

	def question_short(self, obj):
		return truncatechars(obj.question.title, 10)


admin.site.register(Category)
admin.site.register(UserCategoryPreference)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionRating, QuestionRatingAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(AnswerRating, AnswerRatingAdmin)
admin.site.register(Bookmark, BookmarkAdmin)

