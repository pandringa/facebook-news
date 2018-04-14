from .base import JsonScraper, tzs, Article
from dateutil.parser import parse as parse_date
from facebook_news_scraper.models import Article
import re

class ABCNewsScraper(JsonScraper):
  domains = ["abcnews.go.com"]
  # category_map = {
  #   "international": "world",
  #   "health": "lifestyle",
  #   "entertainment": "lifestyle",
  #   "technology": "business",
  #   "travel": "lifestyle",
  #   "us": "national"
  # }
  
  def get_category(self):
    category = super(ABCNewsScraper, self).get_category()
    if category:
      return category

    if self.url:
      slug = re.match('^\/([\w-]+)\/([\w-]+)?\/?', self.url.path)
      categories = []
      if slug:
        if slug.group(1):
          categories.append( slug.group(1) )
        if slug.group(2):
          categories.append( slug.group(2) )
        return '/'.join(categories)

  def get_date(self):
    date = self.html.cssselect('article header .timestamp')
    if date:
      date = date[0].text_content()
      if ' ' in date: ## NOTE this is not a normal space - checks for some unicode character following a dateline
        date = date.split(' ')[1]
      try:
        py_date = parse_date(date, tzinfos=tzs)
        return py_date
      except:
        print("Error parsing date in ABCNewsScraper: %s (url: %s)" % (date, self.url))
    return super(ABCNewsScraper, self).get_date()


  @classmethod
  def categorize(cls, a):
    if isinstance(a, Article):
      pub_cat = a.pub_category
    elif isinstance(a, str):
      pub_cat = a

    category = None
    if pub_cat and '/' in pub_cat:
      sub_cat = pub_cat.split('/')[1].replace('-', ' ')
      category = super(ABCNewsScraper, cls).categorize(sub_cat)
      if not category:
        top_cat = pub_cat.split('/')[0].replace('-', ' ')
        category = super(ABCNewsScraper, cls).categorize(top_cat)
      if category:
        return category

    return super(ABCNewsScraper, cls).categorize(a)