from django.urls import path
from . import views

urlpatterns = [
	path('', views.base, name='base'),
	path('category/<int:category_id>/', views.question_list, name='question_list'),
	path('', views.feed, name='feed'),
	path('popular/', views.popular, name='popular'),
	path('recent/', views.recent, name='recent'),
	path('search/', views.search, name='search'),
	path('create/', views.create_question, name='create_question'),
	path('register/', views.register, name='register'),
	path('question/<int:id>/', views.question_detail, name='question_detail'),
]
