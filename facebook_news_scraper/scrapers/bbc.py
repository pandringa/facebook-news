from .base import JsonScraper

class BBCScraper(JsonScraper):
  domains = ["www.bbc.com", "www.bbc.co.uk"]

  def get_category(self):
    category = super(BBCScraper, self).get_category()
    if category:
      return category

    section = self.html.cssselect('meta[property="og:article:section"]')
    if section:
      return section[0].get('content')

  def get_keywords(self):
    keywords = super(BBCScraper, self).get_keywords()
    if keywords:
      return keywords

    ## Fallback to tags on page
    tags = self.html.cssselect('.tags-list li a')
    if tags:
      return ','.join([tag.text_content() for tag in tags])