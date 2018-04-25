import csv
from dateutil.parser import parse as parse_date
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .models import Page, Post, Article
from django.db.models import Model, Max
from django.db import connection
from .sql_query import all_posts_query, march_april_query, stream_csv

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
  posts = Post.objects
  posts = posts.exclude(page_id__in=EXCLUDE_PAGES)
  posts = posts.exclude(article__category__isnull=True)
  posts = posts.exclude(article__category='local')
  
  if request.GET.get('page'):
    posts = posts.filter(page__slug__in=request.GET.get('page').split(','))
  if request.GET.get('from'):
    posts = posts.filter(posted_at__gte=parse_date(request.GET.get('from')))
  if request.GET.get('to'):
    posts = posts.filter(posted_at__lte=parse_date(request.GET.get('to')))
  posts = posts.order_by('posted_at')

  fields = None # Default to all fields
  if request.GET.get('fields'):
    fields = request.Get.get('fields').split(',')

  print(posts.query)

  return CsvResponse(Post, posts, fields=fields)

# SQL version of get_posts
# GET api/posts/all
def get_all_posts(request):
  cursor =  connection.cursor()
  cursor.execute(march_april_query)
  columns = [col[0] for col in cursor.description]

  return StreamingHttpResponse( 
    stream_csv(columns, cursor), 
    content_type='text/csv'
  )

  # return HttpResponse(
  #   ",".join(columns) + "\n" + "\n".join([
  #     ",".join([str(r) for r in row])
  #   for row in cursor.fetchall()]),
  #   content_type='text/csv'
  # )
    
# GET interactives/top_posts
def top_posts(request):
  reactions = ['like','love','haha','wow','sad','angry', 'comment', 'share']
  posts = []
  for r in reactions:
    val = Post.objects.aggregate(Max(r+'_count'))[r+'_count__max']
    posts.append( Post.objects.get(**{r+'_count': val}) )
  context = {
    'main_domain': 'https://peterandringa.com/facebook-news',
    'reactions': reactions,
    'posts': zip(reactions, posts),
    'width': int(request.GET.get('initialWidth') or 750) - 100
  }
  response = render(request, "top_posts.html", context)
  response['X-Frame-Options'] = 'ALLOW-FROM https://peterandringa.com/'
  return response

