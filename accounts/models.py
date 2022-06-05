from django.db import models
from quizsns_project.settings import EMAIL_BACKEND
from django.core.mail import send_mail
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from django.db import models
from django.utils import timezone



class UserManager(UserManager):

    def _create_user(self, username, loginid, password, **extra_fields):
        if not loginid:
            raise ValueError('The given userid must be set')
        user = self.model(
            username = username,
            loginid = loginid,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, loginid, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, loginid, password, **extra_fields)

    def create_superuser(self, username, loginid, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, loginid, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    loginid = models.CharField(max_length=30, unique=True)
    profile_image = models.FileField(upload_to='profile_image/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)

    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'loginid'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class UserConnect(models.Model):
    from_user_id = models.ForeignKey(
        Users, on_delete=models.CASCADE,
        related_name="from_user_id"
    )
    to_user_id = models.ForeignKey(
        Users, on_delete=models.CASCADE,
        related_name="to_user_id"
    )

    class Meta:
        db_table = 'user_connect'
