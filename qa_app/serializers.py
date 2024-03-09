from rest_framework import serializers
from .models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.get_rating()

    class Meta:
        model = Question
        fields = ['id', 'author', 'title', 'text', 'image', 'pub_date', 'categories', 'rating']



class AnswerSerializer(serializers.ModelSerializer):
	rating = serializers.SerializerMethodField()

	def get_rating(self, obj):
		return obj.get_rating()

	class Meta:
		model = Answer
		fields = ['id', 'user', 'question', 'text', 'pub_date', 'rating']
