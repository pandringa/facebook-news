import json
from .base import Scraper

class CBSNewsScraper(Scraper):
  domains = ["www.cbsnews.com"]

  def __init__(self, res_text, domain):
    super(CBSNewsScraper, self).__init__(res_text, domain)

    json_container = self.html.cssselect('head script[type="application/ld+json"]')
    if json_container:
      try:
        for block in json_container:
          self.json_metadata = json.loads(block.text_content())
          if self.json_metadata['@type'] == 'NewsArticle':
            break
      except:
        self.json_metadata = False
    else:
      self.json_metadata = False

  def get_category(self):
    if self.json_metadata:
      if 'articleSection' in self.json_metadata: 
        return ' - '.join(self.json_metadata['articleSection'])

    return super(CBSNewsScraper, self).get_section()

  def get_date(self):
    if self.json_metadata and 'datePublished' in self.json_metadata:
      return self.json_metadata['datePublished']

    return super(CBSNewsScraper, self).get_date()

  def get_headline(self):
    if self.json_metadata: 
      return self.json_metadata['headline']

    return super(CBSNewsScraper, self).get_headline()

  def get_lede(self):
    if self.json_metadata: 
      return self.json_metadata['description']

    return super(CBSNewsScraper, self).get_lede()

  def get_keywords(self):
    if self.json_metadata:
      if 'keywords' in self.json_metadata: 
        return ','.join(self.json_metadata['keywords'])

    return super(CBSNewsScraper, self).get_keywords()

