import json
from .base import JsonScraper
import re
class USATodayScraper(JsonScraper):
  domains = ["www.usatoday.com", "ftw.usatoday.com"]

  def get_category(self):
    if self.url.host == 'ftw.usatoday.com':
      return 'Sports'
    if self.json_metadata and 'keywords' in self.json_metadata and 'Section:' in self.json_metadata['keywords'][0]:
      return self.json_metadata['keywords'][0]
    return super(USATodayScraper, self).get_category()

  def get_keywords(self):
    # Bypass JSON scraper because USAToday is weird
    keywords = super(JsonScraper, self).get_keywords()
    if not keywords:
      tags = self.html.cssselect('head meta[property="article:tag"]')
      if tags:
        keywords = tags[0].get('content')
    return keywords

  @classmethod
  def categorize(cls, a):
    if a.pub_category:
      category = re.match('Section:(\w+):?(\w+)?', a.pub_category)
      if category:
        if category.group(1) == 'news' and category.group(2):
          category = category.group(2)
        else:
          category = category.group(1)
      elif a.pub_category[0] == '[':
        category = a.pub_category[2:-2]
      
      if category:
        return super(USATodayScraper, cls).categorize(category)
      return super(USATodayScraper, cls).categorize(a)
