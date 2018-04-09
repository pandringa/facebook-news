from .base import JsonScraper, tzs
from dateutil.parser import parse as parse_date
import re

class CNNScraper(JsonScraper):
  domains = ["www.cnn.com", "money.cnn.com", "edition.cnn.com"]

  def get_category(self):
    # Attempt to pull result from meta tags
    result = ""
    section = self.html.cssselect('meta[name="section"]')
    if section:
      result += section[0].get('content')
    subsection = self.html.cssselect('meta[name="subsection"]')
    if subsection:
      result += ' - ' + subsection[0].get('content')
    if result:
      return result

    # Try defaults
    category = super(CNNScraper, self).get_category()
    if category:
      return category

    # Pull from URL
    match = re.search('^/([\w-]+)/.*', self.url.path)
    if match:
      return match.group(1) 

  def get_date(self):
    pubdate = self.html.cssselect('meta[property="og:pubdate"]')
    if not pubdate:
      pubdate = self.html.cssselect('meta[name="pubdate"]')
    if pubdate:
      try:
        py_date = parse_date(pubdate[0].get('content'), tzinfos=tzs)
        return py_date
      except:
        print("Error parsing date in CNNScraper: %s (url: %s)" % (date[0].get('content'), self.url))

    ## Fallback to inferring timezone
    date = super(CNNScraper, self).get_date()
    date_timezone = None
    datestamp = self.html.cssselect('.cnnDateStamp')
    if datestamp:
      for tz in tzs.keys():
        if tz in datestamp[0].text_content():
          date_timezone = tzs[tz]
          break;
    if not date_timezone:
      # Fallback to ET
      date_timezone = tzs["ET"]
    if date:
      return date.replace(tzinfo=date_timezone)
