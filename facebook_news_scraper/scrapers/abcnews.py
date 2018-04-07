from .base import JsonScraper
from dateutil.parser import parse as parse_date
from dateutil.tz import gettz
import re
tzs = {
  "ET": gettz("America/New York"),
  "CT": gettz("America/Chicago"),
  "MT": gettz("America/Denver"),
  "PT": gettz("America/San Francisco")
}

class ABCNewsScraper(JsonScraper):
  domains = ["abcnews.go.com"]

  def get_category(self):
    match = re.search('^/(\w+)/.*', self.url.path)
    if match:
      return match.group(1)
    return super(ABCNewsScraper,self).get_category()

  def get_date(self):
    date = self.html.cssselect('article header .timestamp')
    if date:
      date = date[0].text_content()
      if ' ' in date: ## NOTE this is not a normal space - checks for some unicode character following a dateline
        date = date.split(' ')[1]
      return parse_date(date, tzinfos=tzs)
    return super(ABCNewsScraper, self).get_date()