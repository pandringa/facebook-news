import csv
from dateutil.parser import parse as parse_date
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .models import Page, Post, Article
from django.db.models import Model

# Exclude MSNBC, CNBC, BBC News, Buzzfeed, The Guardian
EXCLUDE_PAGES = ['273864989376427', '97212224368', '228735667216', '21898300328', '10513336322']

class CsvResponse(HttpResponse):
  def __init__(self, cls, data, fields=None):
    super(CsvResponse, self).__init__(content_type='text/csv')

    writer = csv.writer(self)

    
    headers = cls.csv_headers()
    if fields:
      include_ids = [headers.index(f) for f in fields if f in headers]
      headers = [ headers[i] for i in include_ids ]
    
    writer.writerow(headers)

    for model in data:
      data = model.as_csv()
      if fields:
        data = [ data[i] for i in include_ids ]
      writer.writerow(data)

# GET api/pages
def get_pages(request):
  pages = Page.objects.exclude(id__in=EXCLUDE_PAGES)
  return CsvResponse(Page, pages)

# GET api/posts
def get_posts(request):
  posts = Post.objects.exclude(page_id__in=EXCLUDE_PAGES, article__category__isnull=True)
  if request.GET.get('page'):
    posts = posts.filter(page__slug__in=request.GET.get('page').split(','))
  if request.GET.get('from'):
    posts = posts.filter(posted_at__gte=parse_date(request.GET.get('from')))
  if request.GET.get('to'):
    posts = posts.filter(posted_at__lte=parse_date(request.GET.get('to')))
  posts = posts.order_by('posted_at')
  return CsvResponse(Post, posts, fields=request.GET.get('fields').split(','))

