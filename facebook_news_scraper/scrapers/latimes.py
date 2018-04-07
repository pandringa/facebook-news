from .base import Scraper

class LATimesScraper(Scraper):
  domains = ["www.latimes.com"]

  def get_keywords(self):
    return super(LATimesScraper, self).get_keywords() or None