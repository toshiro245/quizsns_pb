import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import (
    QuizCreateForm
)
from .models import (
    QuizPost, QuizList
)
from utils.message_format.make_message_format import (
    home_addquiz_format, 
)


class Homeview(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz_post = QuizPost.objects.order_by('-id')[:12]
        quiz_problems = []
        for quiz in quiz_post:
            quiz_problem = re.sub("\<.*?\>", "", quiz.problem)
            quiz_problems.append(quiz_problem)
        context['quiz_post'] = quiz_post
        context['offset'] = "1"
        context['quiz_problems'] = quiz_problems
        return context


class QuizCreateView(LoginRequiredMixin, CreateView):
    template_name = 'quizpost/quiz_create.html'
    model = QuizPost
    form_class = QuizCreateForm
    success_url = reverse_lazy('quizpost:home')

    # modelにuser情報を格納するための処理
    def form_valid(self, form):
        form.user = self.request.user
        return super().form_valid(form)


class QuizDetailView(DetailView):
    model = QuizPost
    template_name = 'quizpost/quiz_detail.html'

    # いいねをしたクイズのリストを取得して送る
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = self.request.user
            quiz_list = QuizList.objects.filter(user=user)
            liked_list = [quiz.quiz_post.id for quiz in quiz_list]
            context['liked_list'] = liked_list
        except TypeError:
            pass
        return context


class QuizEditView(LoginRequiredMixin, UpdateView):
    template_name = 'quizpost/quiz_edit.html'
    model = QuizPost
    form_class =  QuizCreateForm
    success_url = reverse_lazy('quizpost:home')

    def get(self, request, **kwargs):
        login_user_id = self.request.user.id
        get_object_or_404(QuizPost, pk=self.kwargs['pk'], user_id=login_user_id)
        return super().get(request, **kwargs)

    # modelにuser情報を格納するための処理
    def form_valid(self, form):
        form.user = self.request.user
        return super().form_valid(form)


class QuizDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'quizpost/quiz_delete.html'
    model = QuizPost
    success_url = reverse_lazy('quizpost:home')

    def get(self, request, **kwargs):
        login_user_id = self.request.user.id
        get_object_or_404(QuizPost, pk=self.kwargs['pk'], user_id=login_user_id)
        return super().get(request, **kwargs)
    



@login_required
def quiz_like(request):
    if request.method == "POST":
        quiz_post = get_object_or_404(QuizPost, pk=request.POST.get('quiz_id'))
        user = request.user
        liked = False
        like = QuizList.objects.filter(quiz_post=quiz_post, user=user)
        if like:
            like.delete()
        else:
            like.create(quiz_post=quiz_post, user=user)
            liked = True

        context = {
            'quiz_post_id': quiz_post.id,
            'liked': liked,
            'count': str(quiz_post.quizlist_set.count())
        }
    if request.is_ajax():
        return JsonResponse(context)


def load_quiz(request):
    if request.method == "POST":
        offset = int(request.POST.get('offset'))
        quiz_post = QuizPost.objects.order_by('-id')[offset*12:offset*12+12]
        quiz_post_string = home_addquiz_format(quiz_post)
        offset += 1
        context = {
            'quiz_post': quiz_post_string,
            'offset': offset,
        }
    if request.is_ajax():
        return JsonResponse(context)


# 404error
def page_not_found(request, exception):
    return render(request, 'quizpost/404.html', status=404)

# 500error
def server_error(request):
    return render(request, 'quizpost/500.html', status=500)






