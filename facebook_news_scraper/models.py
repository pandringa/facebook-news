from django.db import models

class Page(models.Model):
  id = models.CharField(max_length=15, primary_key=True, unique=True)
  name = models.CharField(max_length=80)
  slug = models.CharField(max_length=60, unique=True)
  likes = models.IntegerField()

class Article(models.Model):
  url = models.TextField(unique=True)
  category = models.CharField(max_length=80, null=True)
  def clean(self):
    if '?' in self.url:
      self.url = self.url.split('?')[0]

  def save(self, *args, **kwargs):
    self.clean()
    return super().save(*args, **kwargs)

class Post(models.Model):
  id = models.CharField(max_length=60, primary_key=True, unique=True)
  page = models.ForeignKey(Page, on_delete=models.CASCADE)
  post_url = models.CharField(max_length=80)
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  post_text = models.TextField(null=True)
  share_count = models.IntegerField(null=True)
  like_count = models.IntegerField(null=True)
  love_count = models.IntegerField(null=True)
  wow_count = models.IntegerField(null=True)
  haha_count = models.IntegerField(null=True)
  sad_count = models.IntegerField(null=True)
  angry_count = models.IntegerField(null=True)
  comment_count = models.IntegerField(null=True)
  posted_at = models.DateTimeField()

