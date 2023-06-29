from django.shortcuts import render
from .models import Category, Question, Answer
from django.contrib.auth.forms import UserCreationForm


def base(request):
	categories = Category.objects.all()
	return render(request, 'base.html', {'categories': categories})


def question_list(request, category_id):
	questions = Question.objects.filter(category_id=category_id)
	return render(request, 'question_list.html', {'questions': questions})


def feed(request):
	questions = Question.objects.all().order_by('-pub_date')
	return render(request, 'feed.html', {'questions': questions})


def popular(request):
	questions = Question.objects.annotate(num_ratings=Count('questionrating')).order_by('-num_ratings')
	return render(request, 'popular.html', {'questions': questions})


def recent(request):
	questions = Question.objects.all().order_by('-pub_date')
	return render(request, 'recent.html', {'questions': questions})

def search(request):
	query = request.GET.get('query', '')
	results = Question.objects.filter(title__icontains=query)
	return render(request, 'search_results.html', {'results': results})

def create_question(request):
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			question = form.save(commit=False)
			question.author = request.user
			question.save()
			return redirect('question_detail', question.id)
	else:
		form = QuestionForm()
	return render(request, 'create_question.html', {'form': form})