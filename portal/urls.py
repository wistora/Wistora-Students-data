from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('results/<int:attempt_id>/', views.result, name='result'),
    path('history/', views.history, name='history'),
]