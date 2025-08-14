from django.urls import path
from . import views

app_name = 'ai_content_checker'

urlpatterns = [
    path('check-article/', views.check_article_content, name='check_article'),
    path('check-appropriate/', views.check_content_appropriate, name='check_appropriate'),
    path('suggest-improvements/', views.suggest_improvements, name='suggest_improvements'),
]
