from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet
from .views import QuestionSearchViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
	path('', views.base, name='base'),
	path('category/<int:category_id>/', views.question_list, name='question_list'),
	path('feed/', views.feed, name='feed'),
	path('popular/', views.popular, name='popular'),
	path('recent/', views.recent, name='recent'),
	path('search/', views.search, name='search'),
	path('register/', views.register, name='register'),
	path('question/<int:id>/', views.question_detail, name='question_detail'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('login/', views.login_view, name='login'),
	path('bookmark/<int:question_id>/', views.bookmark, name='add_bookmark'),
	path('delete_bookmark/<int:bookmark_id>/', views.delete_bookmark, name='delete_bookmark'),
	path('bookmarks/', views.bookmarks, name='bookmarks'),
	path('question/<int:question_id>/upvote/', views.upvote_question, name='upvote_question'),
	path('question/<int:question_id>/downvote/', views.downvote_question, name='downvote_question'),
	path('answer/<int:answer_id>/upvote/', views.upvote_answer, name='upvote_answer'),
	path('answer/<int:answer_id>/downvote/', views.downvote_answer, name='downvote_answer'),
	path('', include(router.urls)),
	path('questions/search/', QuestionSearchViewSet.as_view({'get': 'list'}), name='question-search'),

]
