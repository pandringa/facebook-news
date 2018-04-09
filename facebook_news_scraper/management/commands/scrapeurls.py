import asyncio
import aiohttp
import async_timeout
import json
from datetime import datetime, date, timezone
import time

from django.core.management.base import BaseCommand, CommandError
from facebook_news_scraper.models import Article, Post, Page
from facebook_news_scraper.config import FB_ACCESS_TOKEN
from facebook_news_scraper.scrapers import by_domain as scrapers

rate_limit = asyncio.Semaphore(25)
total_articles = 0
current_count = 0
errors = []

def safe_fetch(obj,*keys,default=None):
  for key in keys:
    if key in obj:
      obj = obj[key]
    else:
      return default
  return obj

async def fetch_url(session, url):
  async with rate_limit:
    async with async_timeout.timeout(10):
      return await session.get(url)

async def scrape(article):
  async with aiohttp.ClientSession() as session:
    global errors
    try:
      response = await fetch_url(session, article.url)
    except Exception as e:
      print("Error loading ID %i url: %s" % (article.id, article.url))
      errors.append("%i loading: %s" % (article.id, e))
      print(e)
      return

    try:
      text = await response.text()

      if response.url.host in scrapers:
        scraper = scrapers[response.url.host](text, response.url)
        article.scraped = True
      else:
        scraper = scrapers['generic'](text, response.url.host)

      article.pub_date = scraper.get_date()
      article.pub_headline = scraper.get_headline()
      article.pub_lede = scraper.get_lede()
      article.pub_keywords = scraper.get_keywords()
      article.pub_category = scraper.get_category()

      article.resolved_url = response.url
      article.loaded = True
    except Exception as e:
      print("Error setting values on id %i url: %s" % (article.id, article.url))
      errors.append("%i setting values: %s" % (article.id, e))
      print(e)
      return

    try:
      article.save()
    except Exception as e:
      print("Error saving article id %i url: %s" % (article.id, article.url))
      errors.append("%i saving: %s" % (article.id, e))
      print(e)
      return

    global current_count
    global total_count
    current_count += 1
    print("Progress: %i/%i" % (current_count, total_articles), end="\r")

class Command(BaseCommand):
  help = 'Scrapes data from urls'

  def add_arguments(self, parser):
    parser.add_argument('--id', metavar='id', nargs='?')
    parser.add_argument('--page', metavar='page', nargs='?')
    # parser.add_argument('pages', metavar='slug', type=str, nargs='*', help='slug of the page for which to load posts')
    parser.add_argument('--force', dest='force', action='store_true')

  def handle(self, *args, **options):
    articles = Article.objects.all()
    if not options['force']:
      articles = articles.filter(loaded=False)

    if options['id']:
      if '-' in options['id']:
        bounds = options['id'].split('-')
        ids = list(range(int(bounds[0]), int(bounds[1])+1))
      else:
        ids = [int(options['id'])]
      articles = articles.filter(id__in=ids).all()

    if options['page']:
      page_id = Page.objects.get(slug=options['page']).id
      articles = articles.filter(pub_id=page_id)

    global total_articles
    total_articles = len(articles)
    print('\n[%s] Scraping %i URLs...' % (datetime.now(), total_articles))

    loop = asyncio.get_event_loop()

    article_scraping = [scrape(a) for a in articles]
    loop.run_until_complete(asyncio.gather(*article_scraping))
    loop.close()

    with open("logs/scrape.txt", "w") as text_file:
      text_file.write("\n".join(errors))

    print("Finished scraping %i Articles. Wrote %i errors to logs/scrape.txt" % (total_articles, len(errors)))
