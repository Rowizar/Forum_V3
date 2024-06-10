from django.test import TestCase
from django.urls import reverse
from .models import Question

class QuestionTests(TestCase):
    fixtures = ['initial_data.json']

    def test_question_list(self):
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Question")

    def test_question_detail(self):
        question = Question.objects.get(pk=42)
        response = self.client.get(reverse('question_detail', args=[question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a sample question text.")