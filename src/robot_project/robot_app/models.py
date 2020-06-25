from django.db import models
from django.contrib.auth.models import User

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