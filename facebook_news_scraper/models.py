from django.db import models

class Page(models.Model):
  id = models.CharField(max_length=15, primary_key=True, unique=True)
  name = models.CharField(max_length=80)
  page_slug = models.CharField(max_length=30, unique=True)
  likes = models.IntegerField()

class Article(models.Model):
  url = models.CharField(max_length=255, unique=True)
  category = models.CharField(max_length=80)

class Post(models.Model):
  id = models.CharField(max_length=30, primary_key=True, unique=True)
  page = models.ForeignKey(Page, on_delete=models.CASCADE)
  post_url = models.CharField(max_length=80)
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  post_text = models.TextField()
  shares = models.IntegerField()
  likes = models.IntegerField()
  comments = models.IntegerField()

