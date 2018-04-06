import json
from .base import Scraper

class USATodayScraper(Scraper):
  domains = ["www.usatoday.com"]

  def __init__(self, res_text, domain):
    super(USATodayScraper, self).__init__(res_text, domain)

    json_container = self.html.cssselect('head script[type="application/ld+json"]')
    if json_container:
      try:
        self.json_metadata = json.loads(json_container[0].text_content())
      except:
        self.json_metadata = False
    else:
      self.json_metadata = False

  def get_category(self):
    if self.json_metadata:
      if 'keywords' in self.json_metadata:
        return self.json_metadata['keywords'][0]
      if 'articleSection' in self.json_metadata: 
        return self.json_metadata['articleSection']
    else:
      return super(USATodayScraper, self).get_category()

  def get_date(self):
    if self.json_metadata and 'datePublished' in self.json_metadata:
      return self.json_metadata['datePublished']
    else:
      return super(USATodayScraper, self).get_date()

  def get_headline(self):
    if self.json_metadata: 
      return self.json_metadata['headline']
    else:
      return super(USATodayScraper, self).get_headline()

  def get_lede(self):
    if self.json_metadata: 
      return self.json_metadata['description']
    else:
      return super(USATodayScraper, self).get_lede()

  def get_keywords(self):
    keywords = super(USATodayScraper, self).get_keywords()
    if not keywords:
      tags = self.html.cssselect('head meta[property="article:tag"]')
      if tags:
        keywords = tags[0].get('content')
    return keywords

