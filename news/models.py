from django.db import models

# Create your models here.

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    briefSumary = models.CharField(max_length=500)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)

    def __str__(self):
        return self.title
