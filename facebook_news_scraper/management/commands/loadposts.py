import asyncio
import aiohttp
import async_timeout
import json
from datetime import datetime, date, timezone
import time

from django.core.management.base import BaseCommand, CommandError
from facebook_news_scraper.models import Article, Post, Page
from facebook_news_scraper.config import FB_ACCESS_TOKEN

def safe_fetch(obj,*keys,default=None):
  for key in keys:
    if key in obj:
      obj = obj[key]
    else:
      return default
  return obj

async def fetch_url(session, url):
  async with async_timeout.timeout(10):
    async with session.get(url) as response:
      return await response.text()

async def load_posts(page, archive=False):
  async with aiohttp.ClientSession() as session:
    url = 'https://graph.facebook.com/v2.12/'+page.id+'/posts?limit=100&fields=id,permalink_url,created_time,shares,message,link,reactions.type(LIKE).limit(0).summary(1).as(like),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(SAD).limit(0).summary(1).as(sad),reactions.type(ANGRY).limit(0).summary(1).as(angry),comments.limit(0).summary(1)&access_token='+FB_ACCESS_TOKEN
    
    if not archive:
      latest = Post.objects.filter(page=page).order_by('-posted_at').first()
      if not latest:
        print("ERROR: No previous posts found for %s" % page.name)
        return
      latest = latest.posted_at
    else:
      latest = datetime(2018,1,1,tzinfo=timezone.utc)

    url = url + '&since='+ str( int(time.mktime(latest.timetuple())) - 10 ) ## 10 second buffer for rounding errors

    while url:
      shouldContinue = True
      response = await fetch_url(session, url)
      res_json = json.loads(response)
      
      for d in res_json['data']:
        if (not 'link' in d) or ('https://www.facebook.com/' in d['link']): 
          continue

        post = Post(
          id=d['id'],
          page=page,
          post_url=d['permalink_url'],
          post_text=safe_fetch(d, 'message'),
          posted_at=d['created_time'],
          share_count=safe_fetch(d,'shares','count',default=0),
          comment_count=safe_fetch(d,'comments','summary','total_count',default=0),
          like_count=safe_fetch(d,'like','summary','total_count',default=0),
          love_count=safe_fetch(d,'love','summary','total_count',default=0),
          wow_count=safe_fetch(d,'wow','summary','total_count',default=0),
          haha_count=safe_fetch(d,'haha','summary','total_count',default=0),
          sad_count=safe_fetch(d,'sad','summary','total_count',default=0),
          angry_count=safe_fetch(d,'angry','summary','total_count',default=0),
        )

        if ('link' in d) and ('?' in d['link']):
          d['link'] = d['link'].split('?')[0]
        post.article, new_article = Article.objects.get_or_create(url=d['link'])

        post.save()


      url = safe_fetch(res_json,'paging','next')
      if url:
        print("Loading next page from %s... %s" % (page.slug, res_json['data'][-1]['created_time']))
      else:
        print("Done with %s" % page.slug)

class Command(BaseCommand):
  help = 'Loads all recent posts'

  def add_arguments(self, parser):
    parser.add_argument(
      '--archive',
      action='store_true',
      dest='archive',
      help='Build up archive instead of looking for recent posts',
    )
    parser.add_argument('pages', metavar='slug', type=str, nargs='*', help='slug of the page for which to load posts')

  def handle(self, *args, **options):
    pages = Page.objects.all()
    if options['pages']:
      pages = pages.filter(slug__in=options['pages']).all()

    print('\n[%s] Loading posts...' % datetime.now())

    loop = asyncio.get_event_loop()
    
    # Step 1: Load all posts
    post_loading = [load_posts(p, archive=options['archive']) for p in pages]
    loop.run_until_complete(asyncio.gather(*post_loading))

    loop.close()
