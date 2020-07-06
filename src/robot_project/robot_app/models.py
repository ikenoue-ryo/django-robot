from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class User_Question(models.Model):
    user_name = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True)
    question = models.CharField(max_length=50, blank=True, null=True)
    answer = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.question


class GNAVI_Question(models.Model):
    user_name = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True)
    question = models.CharField(max_length=50, blank=True, null=True)
    answer = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.question


class Youtube_Question(models.Model):
    user_name = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True)
    question = models.CharField(max_length=50, blank=True, null=True)
    answer = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.question


SCORE_CHOICES = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]
class Robot_Evaluation(models.Model):
    user_name = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True)
    robot_name = models.CharField('robot_name', max_length=50, blank=True, null=True)
    score = models.PositiveSmallIntegerField(verbose_name='ロボットスコア', choices=SCORE_CHOICES, default='3')

    #ユーザーが同じロボットに2つ以上レビューを書けない設定
    class Meta:
        unique_together = ('robot_name', 'user_name')

    def __str__(self):
        return str(self.robot_name)


class Blog(models.Model):
    user_name = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    text = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    updated_at = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return str(self.title)


# class Blog(models.Model):
#     user_name = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True)
#     celebrity = models.CharField(max_length=50, blank=True, null=True)
#     interest = models.CharField(max_length=150, blank=True, null=True)
#     created_at = models.DateTimeField('作成日', default=timezone.now)
#     updated_at = models.DateTimeField('更新日', default=timezone.now)
#
#     def __str__(self):
#         return str(self.title)