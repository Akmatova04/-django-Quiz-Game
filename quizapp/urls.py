# quizapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Викторинаны баштоо барагы
    path('start/', views.start_quiz_view, name='quiz_start_page'),
    
    # Белгилүү бир ID менен суроону көрсөтүү барагы
    # <int:question_id> - бул URL'ден integer (бүтүн сан) түрүндөгү question_id параметрин алуу
    path('question/<int:question_id>/', views.quiz_view, name='quiz_question_page'),
    
    # Эгер URL'де суроонун ID'си жок болсо (мисалы, /quiz/question/ басылса,
    # бул да quiz_view'га барат, ал жерде биринчи суроого багытталат же ката иштетилет)
    # Бул жолду views.py'дагы логикага жараша алып салса да болот,
    # бирок азыр калтыра туралы.
    path('question/', views.quiz_view, name='quiz_default_question'), 
    
    # Викторинанын жыйынтыктарын көрсөтүү барагы
    path('results/', views.quiz_results_view, name='quiz_results_page'),
]