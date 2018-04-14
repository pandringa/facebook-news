import asyncio
import aiohttp
import async_timeout
import json
from datetime import datetime, timezone
import time
import re
import operator

from urllib.parse import urlparse

from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from facebook_news_scraper.models import Article, Post, Page
from facebook_news_scraper.config import FB_ACCESS_TOKEN
from facebook_news_scraper.scrapers import by_domain as scrapers

rate_limit = asyncio.Semaphore(25)


total_articles = 0
current_count = 0
categorized = 0
errors = []

def categorize(article):
  global total_articles
  global current_count
  global errors
  global categorized

  if article.resolved_url:
    url = urlparse(article.resolved_url)
    if url.hostname in scrapers:
      category = scrapers[url.hostname].categorize(article)
    else:
      category = scrapers['generic'].categorize(article)

    if category:
      article.category = category
      article.save()
      categorized += 1

  current_count += 1
  print("Progress: %i/%i" % (current_count, total_articles), end="\r")

class Command(BaseCommand):
  help = 'Categorizes articles into our classification system'

  def add_arguments(self, parser):
    parser.add_argument('--id', metavar='id', nargs='?')
    parser.add_argument('--page', metavar='page', nargs='?')
    # parser.add_argument('pages', metavar='slug', type=str, nargs='*', help='slug of the page for which to load posts')
    parser.add_argument('--force', dest='force', action='store_true')

  def handle(self, *args, **options):
    global total_articles
    articles = Article.objects.all()

    if not options['force']:
      articles = articles.filter(category__isnull=True)

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

    total_articles = len(articles)
    print('\n[%s] Categorizing %i Articles...' % (datetime.now(), total_articles))

    for a in articles:
      categorize(a)

    with open("logs/scrape.txt", "w") as text_file:
      text_file.write("\n".join(errors))

    print("Successfully categorized %i/%i Articles. Wrote %i errors to logs/scrape.txt" % (categorized, total_articles, len(errors)))
