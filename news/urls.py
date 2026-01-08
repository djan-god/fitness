from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_view, name='newspage'),
    path('<int:id>/', views.news_article_view, name='article_detail')

] 
