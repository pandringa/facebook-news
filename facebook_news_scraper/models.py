from django.db import models

class Page(models.Model):
  id = models.CharField(max_length=15, primary_key=True, unique=True)
  name = models.CharField(max_length=80)
  slug = models.CharField(max_length=60, unique=True)
  likes = models.IntegerField()

  @classmethod
  def csv_headers(cls):
    return ['id', 'name', 'slug', 'likes']

  def as_csv(self):
    return [self.id, self.name, self.slug, self.likes]

class Article(models.Model):
  url = models.TextField(unique=True)
  resolved_url = models.TextField(null=True)
  pub = models.ForeignKey(Page, on_delete=models.CASCADE)
  pub_date = models.DateTimeField(null=True)
  pub_headline = models.TextField(null=True)
  pub_lede = models.TextField(null=True)
  pub_keywords = models.TextField(null=True)
  pub_category = models.CharField(max_length=120, null=True)
  category = models.CharField(max_length=80, null=True)
  loaded = models.BooleanField(default=False)
  scraped = models.BooleanField(default=False)
  total_shares = models.IntegerField(default=0)
  total_comments = models.IntegerField(default=0)
  total_reactions = models.IntegerField(default=0)
  updated_at = models.DateTimeField(null=True)
  def clean(self):
    if '?' in self.url:
      self.url = self.url.split('?')[0]

  def save(self, *args, **kwargs):
    self.clean()
    return super().save(*args, **kwargs)

  Categories = [
    "lifestyle",
    "national",
    "politics",
    "business",
    "science",
    "opinion",
    "sports",
    "world",
    "local",
  ]

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

  @classmethod
  def csv_headers(cls):
    return [
      'page', 
      'fb_id',
      'share_count', 
      'like_count', 
      'love_count',
      'wow_count', 
      'haha_count',
      'sad_count', 
      'angry_count', 
      'comment_count',
      'date',
      'url',
      'category',
    ]

  def as_csv(self):
    return [
      self.page.slug,
      self.id,
      self.share_count,
      self.like_count,
      self.love_count,
      self.wow_count,
      self.haha_count,
      self.sad_count,
      self.angry_count,
      self.comment_count,
      self.posted_at,
      self.article.resolved_url,
      self.article.category
    ]

