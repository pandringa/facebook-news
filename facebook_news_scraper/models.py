from django.db import models

class Page(models.Model):
  id = models.CharField(max_length=15, primary_key=True, unique=True)
  name = models.CharField(max_length=80)
  slug = models.CharField(max_length=60, unique=True)
  likes = models.IntegerField()

class Article(models.Model):
  url = models.TextField(unique=True)
  resolved_url = models.TextField(null=True)
  pub = models.ForeignKey(Page, on_delete=models.CASCADE)
  pub_date = models.DateTimeField(null=True)
  pub_headline = models.TextField(null=True)
  pub_lede = models.TextField(null=True)
  pub_keywords = models.TextField(null=True)
  pub_category = models.CharField(max_length=80, null=True)
  category = models.CharField(max_length=80, null=True)
  loaded = models.BooleanField(default=False)
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
  updated_at = models.DateTimeField()

