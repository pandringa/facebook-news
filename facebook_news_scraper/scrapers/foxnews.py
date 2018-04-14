from .base import JsonScraper
import re

class FoxNewsScraper(JsonScraper):
  domains = ["www.foxnews.com", "www.foxbusiness.com", "insider.foxnews.com"]

  def get_category(self):
    result = ""
    classification = self.html.cssselect('meta[name="classification"]')
    if classification:
      return classification[0].get('content').split(',')[0]
    return super(FoxNewsScraper, self).get_category()

  def get_keywords(self):
    return super(FoxNewsScraper, self).get_keywords() or None

  @classmethod
  def categorize(cls, a):
    if a.pub_category:
      fox_category = re.match('/FOX (NEWS|BUSINESS)/?([\w\s]+)?/?([\w\s]+)?', a.pub_category)
      if fox_category:
        if fox_category.group(1) == 'BUSINESS':
          fox_category = 'business'
        elif fox_category.group(2) == 'NEWS EVENTS':
          fox_category = fox_category.group(3).lower()
        else:
          fox_category = fox_category.group(2).lower()
        return super(FoxNewsScraper, cls).categorize(fox_category)
      return super(FoxNewsScraper, cls).categorize(a)

