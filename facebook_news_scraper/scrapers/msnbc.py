from .base import JsonScraper, tzs
from dateutil.parser import parse as parse_date
import re

class MSNBCScraper(JsonScraper):
  domains = ["www.msnbc.com"]

  def get_category(self):
    category = super(MSNBCScraper,self).get_category()
    if category:
      return category

    tags = self.html.cssselect('meta[property="nv:tags"]')
    if tags:
      return tags[0].get('content')

    # Fallback to URL
    match = re.search('^/([\w-]+)/.*', self.url.path)
    if match:
      return match.group(1)
    
  def get_date(self):
    date = self.html.cssselect('meta[property="nv:date"]')
    if date:
      try:
        date = parse_date(date[0].get('content'), tzinfos=tzs)
        return date
      except:
        print("Error parsing date in MSNBCScraper: %s (url: %s)" % (date[0].get('content'), self.url))
    return super(MSNBCScraper,self).get_date()
    