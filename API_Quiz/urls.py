from django.urls import path
from .views import *

urlpatterns = [
    path('getQuizNames/<str:id>/', get_all_quiz.as_view()),
    path('getQuizNames/', get_all_quiz.as_view()),
    path('Question/', question_paper.as_view()),
    path('attendQuiz/<int:id>/', attend_quiz.as_view()),
]
