import asyncio
import aiohttp
import async_timeout
import json

from django.core.management.base import BaseCommand, CommandError
from facebook_news_scraper.models import Article, Post, Page
from facebook_news_scraper.config import FB_ACCESS_TOKEN

async def fetch_url(session, url):
  async with async_timeout.timeout(10):
    async with session.get(url) as response:
      return await response.text()

async def load_page(slug):
  async with aiohttp.ClientSession() as session:
    response = await fetch_url(session, 'https://graph.facebook.com/v2.12/'+slug+'?fields=fan_count%2Cid%2Cname&access_token='+FB_ACCESS_TOKEN)
    data = json.loads(response)
    page = Page(id=data['id'],slug=slug.lower(),name=data['name'],likes=data['fan_count'])
    page.save()

class Command(BaseCommand):
  help = 'Loads all recent posts'

  def add_arguments(self, parser):
    parser.add_argument('pages', metavar='slug', type=str, nargs='+', help='a page slug to be loaded')

  def handle(self, *args, **options):
    loop = asyncio.get_event_loop()
    tasks = [load_page(s) for s in options['pages']]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
