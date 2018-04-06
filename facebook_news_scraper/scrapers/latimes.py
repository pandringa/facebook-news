from .base import Scraper

class LATimesScraper(Scraper):
  domains = ["www.latimes.com"]


  def get_keywords(self):
    keywords = super(LATimesScraper, self).get_keywords()
    if not keywords:
      keywords = self.html.cssselect('head meta[property="article:tag"]')
      if keywords:
        keywords = keywords[0].get('content') or None

    return keywords or None
