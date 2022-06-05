import re

from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from accounts.forms import (
    UserCreationForm, UserLoginForm, UserEditForm, UserPasswordChangeForm, 
)
from accounts.models import UserConnect
from quizpost.models import QuizList, QuizPost
from utils.message_format.make_message_format import (
    detail_addmyquiz_format, detail_addlikequiz_format,
)


User = get_user_model()


class UserRegist(CreateView):
    template_name = 'accounts/user_regist.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        try:
            form.save()
        except ValidationError as e:
            form.add_error('password', e)
            return render(self.request, 'accounts/user_regist.html', context={
            'form': form,
        })

        return redirect('accounts:user_create_done')


class UserCreateDone(TemplateView):
    template_name = 'accounts/user_create_done.html'


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    pass


class UserEditView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/user_edit.html'
    model = User
    form_class = UserEditForm

    def get(self, request, **kwargs):
        login_user_id = self.request.user.id
        edit_user_id = self.kwargs['pk']
        if login_user_id != edit_user_id:
            raise Http404
        return super().get(request, **kwargs)

    def get_success_url(self):
        return reverse_lazy('accounts:user_detail', kwargs={"pk":self.kwargs["pk"]})


# ユーザ情報確認画面
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz_list = QuizPost.objects.filter(user_id=self.kwargs['pk']).order_by('-id')[:6]
        context['quiz_list'] = quiz_list
        liked_quiz_list = QuizList.objects.filter(user_id=self.kwargs['pk']).order_by('-quiz_post')[:6]
        context['liked_quiz_list'] = liked_quiz_list
        myquiz_offset = 1
        likequiz_offset = 1
        context['myquiz_offset'] = myquiz_offset
        context['likequiz_offset'] = likequiz_offset

        # 訪問したユーザーがそのページのユーザーをお気に入り登録しているかどうか
        loginuser_favorite = UserConnect.objects.filter(
                 from_user_id = self.request.user.id,
                 to_user_id = self.kwargs['pk']
                 )
        if loginuser_favorite:
            context['loginuser_favorite'] = True

        # 訪問したページのユーザーがお気に入り登録しているユーザーを全て取得
        favorite_users =  UserConnect.objects.filter(
                 from_user_id = self.kwargs['pk']
                 ).all()

        context['favorite_users'] = favorite_users

        # 初期表示されるクイズの問題の処理
        my_quiz_problems = []
        liked_quiz_problems = []
        for quiz in quiz_list:
            quiz_problem = re.sub("\<.*?\>", "", quiz.problem)
            my_quiz_problems.append(quiz_problem)
        
        for quiz in liked_quiz_list:
            quiz_problem = re.sub("\<.*?\>", "", quiz.quiz_post.problem)
            liked_quiz_problems.append(quiz_problem)

        context['my_quiz_problems'] = my_quiz_problems
        context['liked_quiz_problems'] = liked_quiz_problems
        return context


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/user_password_change.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('accounts:user_password_change_done')


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/user_password_change_done.html'


# Passwordを忘れた場合の処理
# class UserPasswordResetView(PasswordResetView):
#     template_name = 'accounts/user_password_reset.html'
#     form_class = UserPasswordResetForm
#     subject_template_name = 'accounts/mail_template/password_forget_subject.txt'
#     email_template_name = 'accounts/mail_template/password_forget_message.txt'
#     success_url = reverse_lazy('accounts:user_password_reset_done')


# class UserPasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'accounts/user_password_reset_done.html'


# class UserPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'accounts/user_password_reset_confirm.html'
#     form_class = UserSetPasswordForm
#     success_url = reverse_lazy('accounts:user_password_reset_complete')


# class UserPasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = 'accounts/user_password_reset_complete.html'




# マイページの自分のクイズ読み込み
@login_required
def load_mypage_myquiz(request):
    if request.method == "POST":
        user_id = int(request.POST.get('user_id'))
        offset = int(request.POST.get('myquiz_offset'))
        my_quiz_list = QuizPost.objects.filter(user_id=user_id).order_by('-id')[offset*6:offset*6+6]
        my_quiz_list_string = detail_addmyquiz_format(my_quiz_list)
        offset += 1
        context = {
            'my_quiz_list': my_quiz_list_string,
            'myquiz_offset': offset,
        }
    if request.is_ajax():
        return JsonResponse(context)


# マイページのいいねしたクイズ読み込み
@login_required
def load_mypage_likequiz(request):
    if request.method == "POST":
        user_id = int(request.POST.get('user_id'))
        offset = int(request.POST.get('likequiz_offset'))
        liked_quiz_list = QuizList.objects.filter(user_id=user_id).order_by('-quiz_post')[offset*6:offset*6+6]
        liked_quiz_list_string = detail_addlikequiz_format(liked_quiz_list)
        offset += 1
        context = {
            'like_quiz_list': liked_quiz_list_string,
            'likequiz_offset': offset,
        }
    if request.is_ajax():
        return JsonResponse(context)


# お気に入りのユーザー登録
@login_required
def favorite_user_rigist(request):
    if request.method == "POST":
        favorite = False
        to_user_id = int(request.POST.get('user_id'))
        to_user = get_object_or_404(User, id=to_user_id)
        from_user = request.user
        user_connect, created = UserConnect.objects.get_or_create(
            from_user_id = from_user,
            to_user_id = to_user,
        )
        if created:
            favorite = True
        else:
            favorite = False
            user_connect.delete()
        
        context = {
            'favorite': favorite,
        }
            

    if request.is_ajax():
        return JsonResponse(context)


    
    




    
