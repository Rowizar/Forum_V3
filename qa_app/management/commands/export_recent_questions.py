import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from qa_app.models import Question


class Command(BaseCommand):
	help = 'Export questions from the last month to a CSV file'

	def add_arguments(self, parser):
		parser.add_argument('filename', type=str, help='The CSV filename where to export questions')

	def handle(self, *args, **options):
		today = timezone.now()
		one_month_ago = today - timedelta(days=30)

		recent_questions = Question.objects.filter(pub_date__gte=one_month_ago)

		with open(options['filename'], mode='w', newline='', encoding='utf-8') as file:
			writer = csv.writer(file)
			writer.writerow(['ID', 'Title', 'Author', 'Publication Date'])

			for question in recent_questions:
				writer.writerow([
					question.pk,
					question.title,
					question.author.username,
					question.pub_date.strftime('%Y-%m-%d %H:%M:%S')
				])

			self.stdout.write(self.style.SUCCESS(
				f'Successfully exported {recent_questions.count()} questions to {options["filename"]}'))
