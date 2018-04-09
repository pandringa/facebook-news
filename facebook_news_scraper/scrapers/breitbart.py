from .base import JsonScraper

class BreitbartScraper(JsonScraper):
  domains = ["www.breitbart.com"]

  def get_category(self):
    section = self.html.cssselect('[property="article:section"]')
    if section:
      return section[0].get('content')
    return super(BreitbartScraper, self).get_category()

  def get_keywords(self):
    if self.json_metadata and 'keywords' in self.json_metadata:
      return self.json_metadata['keywords']

    return super(BreitbartScraper, self).get_keywords()