from django.contrib import admin
from .models import User_Question, GNAVI_Question, Youtube_Question


class User_QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'question',
    'answer')
    list_display_links = ('id', 'user_name')


admin.site.register(User_Question, User_QuestionAdmin)


class GNAVI_QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'question',
    'answer')
    list_display_links = ('id', 'user_name')


admin.site.register(GNAVI_Question, GNAVI_QuestionAdmin)



class Youtube_QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'question',
    'answer')
    list_display_links = ('id', 'user_name')


admin.site.register(Youtube_Question, Youtube_QuestionAdmin)