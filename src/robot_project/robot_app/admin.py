from django.contrib import admin
from .models import User_Question, GNAVI_Question, Youtube_Question, Robot_Evaluation, Blog


class User_QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'question', 'answer')
    list_display_links = ('id', 'user_name')


admin.site.register(User_Question, User_QuestionAdmin)


class GNAVI_QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'question', 'answer')
    list_display_links = ('id', 'user_name')


admin.site.register(GNAVI_Question, GNAVI_QuestionAdmin)



class Youtube_QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'question', 'answer')
    list_display_links = ('id', 'user_name')


admin.site.register(Youtube_Question, Youtube_QuestionAdmin)


class Robot_EvaluationAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'robot_name', 'score')
    list_display_links = ('robot_name', 'user_name')

admin.site.register(Robot_Evaluation, Robot_EvaluationAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'title', 'text', 'created_at')
    list_display_links = ('user_name', 'title')

admin.site.register(Blog, BlogAdmin)