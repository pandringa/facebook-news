import asyncio
import aiohttp
import async_timeout
import json
from datetime import datetime

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

def split_chunks(l, n):
  for i in range(0, len(l), n):
    yield l[i:i + n]

async def fetch_url(session, url):
  async with async_timeout.timeout(10):
    async with session.get(url) as response:
      return await response.text()

# Refresh stats for up to 50 posts at a time
async def refresh_stats(by_id):
  url = 'https://graph.facebook.com/v2.12/?ids='+ ','.join(by_id.keys()) +'&fields=shares.limit(0).summary(1),reactions.type(LIKE).limit(0).summary(1).as(like),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(SAD).limit(0).summary(1).as(sad),reactions.type(ANGRY).limit(0).summary(1).as(angry),comments.limit(0).summary(1)&access_token='+FB_ACCESS_TOKEN
  
  async with aiohttp.ClientSession() as session:
    response = await fetch_url(session, url)
    for post_id, stats in json.loads(response).items():
      post = by_id[post_id]
      post.like_count =     safe_fetch(stats,'like','summary','total_count',default=0)
      post.love_count =     safe_fetch(stats,'love','summary','total_count',default=0)
      post.wow_count =      safe_fetch(stats,'wow','summary','total_count',default=0)
      post.haha_count =     safe_fetch(stats,'haha','summary','total_count',default=0)
      post.sad_count =      safe_fetch(stats,'sad','summary','total_count',default=0)
      post.comment_count =  safe_fetch(stats,'comments','summary','total_count',default=0)
      post.share_count =    safe_fetch(stats,'shares','count',default=0)
      post.save()

class Command(BaseCommand):
  help = 'Updates like, comment, and share counts for all posts'

  def add_arguments(self, parser):
    parser.add_argument('pages', metavar='slug', type=str, nargs='*', help='a page slug to be loaded')

  def handle(self, *args, **options):
    posts = Post.objects.all()
    if options['pages']:
      pages = Page.objects.filter(slug__in=options['pages']).values('id')
      posts = posts.filter(page_id__in=pages)

    print('\n[%s] Refreshing stats for %s posts...' % (datetime.now(), len(posts)))

    batched_array = split_chunks(list(posts), 50)
    batched_dicts = [{post.id: post for post in arr} for arr in batched_array]

    loop = asyncio.get_event_loop()
    tasks = [refresh_stats(by_id) for by_id in batched_dicts]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
