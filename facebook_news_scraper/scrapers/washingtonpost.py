from .base import JsonScraper
import re
from dateutil.parser import parse as parse_date

class WashingtonPostScraper(JsonScraper):
  domains = ["www.washingtonpost.com"]

  def get_category(self):
    result = ""
    match = re.search('^/(\w+)/.*', self.url.path)
    if match and match.group(1):
      result += match.group(1) + ' - '

    category_link = self.html.cssselect('section#top-content .headline-kicker a.kicker-link')
    if category_link:
      result += category_link[0].text_content()

    if result:
      return result  
    return super(WashingtonPostScraper,self).get_category()

  def get_date(self):
    date = super(WashingtonPostScraper,self).get_date()
    if not date:
      date = self.html.cssselect('[itemprop="datePublished"]')
      if date and date[0].get('content'):
        return parse_date(date[0].get('content'))
    else:
      return date

