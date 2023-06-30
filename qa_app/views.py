from django.db.models import Count
from django.shortcuts import render, redirect
from .forms import QuestionForm
from .models import Category, Question, Answer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
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


@login_required(login_url='/login/')
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


def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')  # предполагается, что у вас есть маршрут и представление для входа
	else:
		form = UserCreationForm()
	return render(request, 'register.html', {'form': form})
