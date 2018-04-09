from .base import Scraper, tzs
from dateutil.parser import parse as parse_date

class NYTimesScraper(Scraper):
  domains = ["www.nytimes.com", "cooking.nytimes.com"]

  def get_category(self):
    if self.url.host == 'cooking.nytimes.com':
      return 'Recipes'
    else:
      return super(NYTimesScraper, self).get_category()

  def get_date(self):
    article_published = self.html.cssselect('head meta[property="article:published"]')
    if not article_published:
      article_published = self.html.cssselect('head meta[name="ptime"]')
    if not article_published:
      article_published = self.html.cssselect('head meta[name="pdate"]')

    if article_published: 
      date = parse_date(article_published[0].get('content'), tzinfos=tzs)
      if not date.tzinfo:
        date = date.replace(tzinfo=tzs['ET'])
      return date
    else:
      return super(NYTimesScraper, self).get_date()