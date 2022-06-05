from django.contrib import admin
from django.urls import path

from .views import (
    UserRegist, UserCreateDone, UserLoginView,
    UserLogoutView, UserEditView, UserDetailView, load_mypage_myquiz, 
    load_mypage_likequiz, favorite_user_rigist, UserPasswordChangeView, 
    UserPasswordChangeDoneView, 
)

app_name = 'accounts'


urlpatterns = [
    path('user_regist', UserRegist.as_view(), name='user_regist'),
    path('user_create_done', UserCreateDone.as_view(),name='user_create_done'),
    # path('user_create_complete/<token>', UserCreateComplete.as_view(), name='user_create_complete'),
    path('user_login', UserLoginView.as_view(), name='user_login'),
    path('user_logout', UserLogoutView.as_view(), name='user_logout'),
    path('user_edit/<int:pk>', UserEditView.as_view(), name='user_edit'),
    path('user_detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('load_mypage_myquiz/', load_mypage_myquiz, name='load_mypage_myquiz'),
    path('load_mypage_likequiz/', load_mypage_likequiz, name='load_mypage_likequiz'),
    path('favorite_user_regist/', favorite_user_rigist, name='favorite_user_rigist'),
    path('user_password_change/', UserPasswordChangeView.as_view(), name='user_password_change'),
    path('user_password_change_done/', UserPasswordChangeDoneView.as_view(), name='user_password_change_done'),
]

