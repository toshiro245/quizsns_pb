from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class QuizPost(models.Model):
    title = models.CharField(max_length=50)
    problem = models.TextField()
    hint = models.CharField(max_length=1000, null=True, blank=True)
    answer = models.TextField()
    create_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'quiz_post'


class QuizList(models.Model):
    quiz_post = models.ForeignKey(
        QuizPost, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'quiz_list'



