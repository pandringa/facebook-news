from json import loads
from html import unescape
from lxml.html import fromstring
from dateutil.parser import parse as parse_date
from dateutil.tz import gettz

tzs = {
  "ET": gettz("America/New York"),
  "CT": gettz("America/Chicago"),
  "MT": gettz("America/Denver"),
  "PT": gettz("America/San Francisco"),
  "EST": gettz("America/New York"),
  "CST": gettz("America/Chicago"),
  "MST": gettz("America/Denver"),
  "PST": gettz("America/San Francisco"),
  "EDT": gettz("America/New York"),
  "CDT": gettz("America/Chicago"),
  "MDT": gettz("America/Denver"),
  "PDT": gettz("America/San Francisco"),
}

# Base Scraper for others to inherit from
class Scraper:
  domains = []

  def __init__(self, res_text, url):
    self.html = fromstring(res_text)
    self.url = url

  def get_category(self):
    article_section = self.html.cssselect('meta[property="article:section"]')
    if article_section:
      return article_section[0].get('content')

  def get_date(self):
    date = self.html.cssselect('meta[property="article:published"]')
    if not date:
      date = self.html.cssselect('meta[property="article:published_time"]')
    if not date:
      date = self.html.cssselect('meta[name="date"]')
    if date:
      try:
        py_date = parse_date(date[0].get('content'), tzinfos=tzs)
        return py_date
      except:
        global date
        print("Error parsing date: %s (url: %s)" % (date[0].get('content'), self.url))

  def get_headline(self):
    article_headline = self.html.cssselect('meta[property="og:title"]')
    if article_headline: 
      return unescape(article_headline[0].get('content'))

  def get_lede(self):
    description = self.html.cssselect('meta[name="description"]')
    if not description:
      description = self.html.cssselect('meta[property="og:description"]')

    if description: 
      return unescape(description[0].get('content'))

  def get_keywords(self):
    keywords = self.html.cssselect('meta[name="news_keywords"]')
    if not keywords:
      keywords = self.html.cssselect('meta[name="keywords"]')
    if not keywords:
      keywords = self.html.cssselect('meta[property="article:tag"]')
    if not keywords:
      keywords = self.html.cssselect('meta[property="og:article:tag"]')

    if keywords: return keywords[0].get('content')

class JsonScraper(Scraper):
  domains = ['generic']

  def __init__(self, res_text, domain):
    super(JsonScraper, self).__init__(res_text, domain)

    json_container = self.html.cssselect('script[type="application/ld+json"]')
    if json_container:
        for block in json_container:
          try:
            self.json_metadata = loads(block.text_content())
          except:
            self.json_metadata = False
          if self.json_metadata and '@type' in self.json_metadata and (self.json_metadata['@type'] == 'NewsArticle' or self.json_metadata['@type'] == 'ReportageNewsArticle'):
            break
    else:
      self.json_metadata = False

  def get_category(self):
    if self.json_metadata and 'articleSection' in self.json_metadata: 
      return self.json_metadata['articleSection']
    return super(JsonScraper, self).get_category()

  def get_date(self):
    if self.json_metadata and 'datePublished' in self.json_metadata:
      try:
        py_date = parse_date(self.json_metadata['datePublished'], tzinfos=tzs)
        return py_date
      except:
        print("Error parsing date: %s (url: %s)" % (date[0].get('content'), self.url))

    return super(JsonScraper, self).get_date()

  def get_headline(self):
    if self.json_metadata and 'headline' in self.json_metadata: 
      return unescape(self.json_metadata['headline'])
    return super(JsonScraper, self).get_headline()

  def get_lede(self):
    if self.json_metadata and 'description' in self.json_metadata and self.json_metadata['description']: 
      return unescape(self.json_metadata['description'])
    return super(JsonScraper, self).get_lede()

  def get_keywords(self):
    if self.json_metadata and 'keywords' in self.json_metadata and self.json_metadata['keywords']: 
        return ','.join(self.json_metadata['keywords'])
    return super(JsonScraper, self).get_keywords()