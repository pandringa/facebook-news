import json
from .base import JsonScraper

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

