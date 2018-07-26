import asyncio
import aiohttp
import async_timeout
import json
from datetime import datetime, timezone

from django.core.management.base import BaseCommand, CommandError
from facebook_news_scraper.models import Article, Post, Page
from facebook_news_scraper.config import FB_ACCESS_TOKEN

rate_limit = asyncio.Semaphore(20)
count = 0
global count
def safe_fetch(obj,*keys,default=None):
  for key in keys:
    if key in obj:
      obj = obj[key]
    else:
      return default
  return obj

def split_chunks(l, n):
  for i in range(0, len(l), n):
    yield l[i:i + n]

def count_diffs(a,b):
  return sum( a[i] != b[i] for i in range(min(len(a),len(b))) )

async def fetch_url(session, url):
  async with rate_limit:
    async with async_timeout.timeout(10):
      async with session.get(url) as response:
        return (await response.text(), response.headers)

# Refresh stats for up to 50 posts at a time
async def refresh_shares(by_url):
  global count
  url = 'https://graph.facebook.com/v3.0/?fields=engagement&ids='+ (','.join(by_url.keys()))+'&access_token='+FB_ACCESS_TOKEN
  async with aiohttp.ClientSession() as session:
    response, headers = await fetch_url(session, url)
    for a_url, stats in json.loads(response).items():
      if a_url == 'error':
        print(headers)
        print('ERROR in request: %s' % response);
      
      article = False
      if a_url in by_url:
        article = by_url[a_url]
      else:
        a_url = a_url.split('?')[0].split('&')[0]
        if a_url in by_url:
          article = by_url[a_url]
        else:
          for url in by_url.keys():
            diff = count_diffs(url, a_url)
            if diff < 2:
              article = by_url[url]
              break 

      if not article:
        print('Could not match urls', a_url)
        return

      article.total_shares = safe_fetch(stats,'engagement','share_count',default=0)
      article.total_comments = safe_fetch(stats,'engagement','comment_count',default=0)
      article.total_reactions = safe_fetch(stats,'engagement','reaction_count',default=0)
      article.updated_at = datetime.now(timezone.utc)
      article.save()
      if not article.updated_at:
        print('No Updated_At for article ID %s' % article.id)
      else:
        count += 1

class Command(BaseCommand):
  help = 'Updates total shares for each article'

  def add_arguments(self, parser):
    parser.add_argument('pages', metavar='slug', type=str, nargs='*', help='a page slug to be loaded')
    parser.add_argument('--chunk', nargs=1, type=int, help='Chunk number (out of 24)')

  def handle(self, *args, **options):
    articles = Article.objects.order_by('id').all()
    count = Article.objects.count()

    if options['pages']:
      pages = Page.objects.filter(slug__in=options['pages']).values('id')
      articles = articles.filter(pub_id__in=pages)
        
    if options['chunk']:
      start = int( options['chunk'][0] * count / 24.0 )
      end = int( (options['chunk'][0]+1) * count / 24.0 )
      print('Loading article stats chunk %s (for articles ids %s to %s):' % (options['chunk'][0], articles[start].id, articles[end].id))
      articles = articles[ start : end ]
    
    count = articles.count()
    pointer = 0
    batch_size = 5000
    loop = asyncio.get_event_loop()

    while pointer < count:
      
      articles_part = articles[pointer : (pointer + batch_size)]
      print('\n[%s] Refreshing total-shares for %s articles...' % (datetime.now(), len(articles_part)))

      batched_array = split_chunks(list(articles_part), 49)
      batched_dicts = [{ (article.resolved_url or article.url).split('?')[0]: article for article in arr} for arr in batched_array]
      
      tasks = [refresh_shares(by_url) for by_url in batched_dicts]

      pointer += batch_size

      loop.run_until_complete(asyncio.gather(*tasks))
      
      print('Completed %s refreshes.' % count)
    loop.close()
