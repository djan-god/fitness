from django.shortcuts import render
from .models import NewsArticle

# Create your views here.

def news_view(request):
    news_articles = NewsArticle.objects.all().order_by('-published_date')
    return render(request, 'news/news_page.html', {'news_articles': news_articles})

def news_article_view(request, id):
    article = NewsArticle.objects.get(id=id)
    return render(request, 'news/news_article.html', {'newsArticle': article})