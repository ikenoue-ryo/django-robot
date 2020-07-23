from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import views

app_name = 'robot_app'

urlpatterns = [
    path('', login_required(views.indexfunc), name='index'),
    path('detail/<int:pk>/', views.detailfunc, name='detail'),
    path('update/<int:pk>/', views.updatefunc, name='update'),
    path('signup/', views.signupfunc, name='signup'),
    path('login/', views.loginfunc, name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('g_navi/', views.g_navi, name='g_navi'),
    path('youtube/', views.youtube, name='youtube'),
    path('add_questions/', views.add_questions, name='add_questions'),
    path('morning/', views.morning, name='morning'),
    path('morning/edit/<int:pk>/', views.morning_edit, name='morning_edit'),
    path('blog_create/', views.blog_create, name='blog_create'),
    path('news/', views.news, name='news'),
    path('mycalendar/', views.MyCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
    path('mycalendar/', views.MyCalendar.as_view(), name='mycalendar'),
    path('mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'),
    path('month_with_schedule/', views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('month_with_schedule/<int:year>/<int:month>/', views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('net_shop/', views.net_shop, name='net_shop'),
    path('shop_detail/<str:itemId>/', views.shop_detail, name='shop_detail'),
    path('map/', views.map, name='map'),
    path('robot_review/', views.robot_review, name='robot_review'),
    path('notify/', views.notify, name='notify'),
    path('week_tenki/', views.week_tenki, name='week_tenki'),
    path('any_questions/', views.any_questions, name='any_questions'),
    path('ajax_answer_add/', views.ajax_answer_add, name='ajax_answer_add'),
]