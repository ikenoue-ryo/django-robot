from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import views

app_name = 'robot_app'

urlpatterns = [
    path('', login_required(views.indexfunc), name='index'),
    path('detail/<int:pk>/', views.detailfunc, name='detail'),
    path('signup/', views.signupfunc, name='signup'),
    path('login/', views.loginfunc, name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('g_navi/', views.g_navi, name='g_navi'),
    path('youtube/', views.youtube, name='youtube'),
    path('add_questions/', views.add_questions, name='add_questions'),

]