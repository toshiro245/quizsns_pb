from datetime import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm, ReadOnlyPasswordHashField, PasswordChangeForm,
)
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator



User = get_user_model()


class UserCreationForm(forms.ModelForm):
    loginid = forms.CharField(label='LoginID (6文字以上)', validators=[MinLengthValidator(6)])
    password = forms.CharField(label='Password (8文字以上)', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Password再入力', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'loginid', 'password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = str(field.label) + '*'
            field.widget.attrs['class'] = 'form-control'


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません')

    def save(self, commit=False):
        user = super().save(commit=False)
        user.is_active = True
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


# 管理画面のUser編集用Form
class UserChangeForm(forms.ModelForm):
    create_at = forms.DateTimeField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    password = ReadOnlyPasswordHashField()
    profile_image = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ('username', 'loginid', 'profile_image', 'password', 'is_staff', 'is_active', 'is_superuser', 'create_at', 'update_at')

    def clean_password(self):
        return self.initial['password']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='LoginID')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    remember = forms.BooleanField(label='ログイン状態を保持する', required=False)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['remember'].widget.attrs['class'] = 'form-remember'
        self.fields['username'].widget.attrs['placeholder'] = str(self.fields['username'].label) + '*'
        self.fields['password'].widget.attrs['placeholder'] = str(self.fields['password'].label) + '*'


# マイページから編集するようのform
class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    loginid = forms.CharField(label='LoginID (6文字以上)', validators=[MinLengthValidator(6)])
    profile_image = forms.FileField(label='Image', required=False)

    class Meta:
        model = User
        fields = ('username', 'loginid', 'profile_image')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['loginid'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = str(self.fields['username'].label) + '*'
        self.fields['loginid'].widget.attrs['placeholder'] = str(self.fields['loginid'].label) + '*'

    def save(self, commit=False):
        user = super().save(commit=False)
        print(user.profile_image)
        print('きた')
        user.update_at = datetime.now()
        user.save()
        return user


# PasswordChange
class UserPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            
            field.widget.attrs['class'] = 'form-control'


# パスワード忘れた場合
# class UserPasswordResetForm(PasswordResetForm):

#     def __init__(self, *args, **kwargs):
#         super(UserPasswordResetForm, self).__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'


# class UserSetPasswordForm(SetPasswordForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'



    

        