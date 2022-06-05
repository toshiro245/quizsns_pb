from django.urls import path

from .views import (
    Homeview, QuizCreateView, QuizDetailView, quiz_like, load_quiz,
    QuizEditView, QuizDeleteView

)

app_name = 'quizpost'

urlpatterns = [
    path('home/', Homeview.as_view(), name='home'),
    path('quiz_create/', QuizCreateView.as_view(), name='quiz_create'),
    path('quiz_detail/<int:pk>', QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz_like/', quiz_like, name='quiz_like'),
    path('load_quiz/', load_quiz, name='load_quiz'),
    path('quiz_edit/<int:pk>', QuizEditView.as_view(), name='quiz_edit'),
    path('quiz_delete/<int:pk>', QuizDeleteView.as_view(), name='quiz_delete'),
]