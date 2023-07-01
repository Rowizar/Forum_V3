from django.db.models import Count
from django.shortcuts import render, redirect
from .forms import QuestionForm
from .models import Category, Question, Answer, Bookmark
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render
from .models import Question
from .forms import AnswerForm


def base(request):
	categories = Category.objects.all()
	if request.method == 'POST' and request.user.is_authenticated:
		form = QuestionForm(request.POST)
		if form.is_valid():
			question = form.save(commit=False)
			question.author = request.user
			question.save()
			return redirect('question_detail', question.id)
	else:
		form = QuestionForm()
	return render(request, 'base.html', {'categories': categories, 'form': form})


def question_list(request, category_id):
	questions = Question.objects.filter(category_id=category_id)
	return render(request, 'feed.html', {'questions': questions})


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


def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')  # предполагается, что у вас есть маршрут и представление для входа
	else:
		form = UserCreationForm()
	return render(request, 'register.html', {'form': form})


def question_detail(request, id):
	question = get_object_or_404(Question, id=id)
	answers = Answer.objects.filter(question=question)

	bookmark = None
	if request.user.is_authenticated:
		bookmark = Bookmark.objects.filter(user=request.user, question=question).first()

	if request.method == 'POST' and request.user.is_authenticated:
		form = AnswerForm(request.POST)
		if form.is_valid():
			answer = form.save(commit=False)
			answer.user = request.user
			answer.question = question
			answer.save()
			return redirect('question_detail', question.id)  # Обновить страницу с новым ответом
	else:
		form = AnswerForm()

	return render(request, 'question_detail.html',
				  {'question': question, 'answers': answers, 'form': form, 'bookmark': bookmark})


def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('base')
		else:
			# Invalid username or password
			return render(request, 'login.html', {'error': 'Invalid username or password'})
	else:
		return render(request, 'login.html')


def bookmark(request, question_id):
	question = get_object_or_404(Question, id=question_id)
	Bookmark.objects.create(user=request.user, question=question)
	return redirect('feed')  # или куда вам нужно перенаправить пользователя после добавления в закладки


def delete_bookmark(request, bookmark_id):
	bookmark = get_object_or_404(Bookmark, id=bookmark_id, user=request.user)
	bookmark.delete()
	return redirect('bookmarks')  # или куда вам нужно перенаправить пользователя после удаления из закладок


def bookmarks(request):
	bookmarks = Bookmark.objects.filter(user=request.user)
	return render(request, 'bookmarks.html', {'bookmarks': bookmarks})
