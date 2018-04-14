from .base import Scraper

class LATimesScraper(Scraper):
  domains = ["www.latimes.com"]
  # category_map = {
  #   'tech': 'business',
  #   'entertainment': 'lifestyle',
  #   'books': 'lifestyle',
  #   'california living': 'lifestyle',
  #   'nation': 'national',
  #   'us': 'national',
  #   'travel': 'lifestyle',
  #   'essential politics': 'politics',
  #   'food': 'lifestyle',
  #   'home & garden': 'lifestyle',
  #   'fashion': 'lifestyle',
  #   'olympics': 'sports',
  #   'essential washington': 'politics',
  #   'health & wellness': 'lifestyle',
  #   'education': 'national'
  # }

  def get_keywords(self):
    return super(LATimesScraper, self).get_keywords() or None

  @classmethod
  def categorize(cls, a):
    if a.pub_category:
      categories = list(filter(None, a.pub_category.split(',')))
      if len(categories) >= 2:
        return super(LATimesScraper, cls).categorize(categories[-2].lower().strip())
      return super(LATimesScraper, cls).categorize(a)
