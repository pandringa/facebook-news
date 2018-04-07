from .base import JsonScraper

class FoxNewsScraper(JsonScraper):
  domains = ["www.foxnews.com", "www.foxbusiness.com", "http://insider.foxnews.com"]

  def get_category(self):
    result = ""
    classification = self.html.cssselect('meta[name="classification"]')
    if classification:
      return classification[0].get('content').split(',')[0]
    return super(FoxNewsScraper, self).get_category()

  def get_keywords(self):
    return super(FoxNewsScraper, self).get_keywords() or None