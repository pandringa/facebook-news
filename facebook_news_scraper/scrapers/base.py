from lxml.html import fromstring

# Base Scraper for others to inherit from
class Scraper:
  domains = ['generic']

  def __init__(self, res_text, domain):
    self.html = fromstring(res_text)
    self.domain = domain

  def get_category(self):
    article_section = self.html.cssselect('meta[property="article:section"]')
    if article_section:
      return article_section[0].get('content')

  def get_date(self):
    date = self.html.cssselect('meta[property="article:published"]')
    if not date:
      date = self.html.cssselect('meta[name="date"]')
    if date:
      return date[0].get('content')

  def get_headline(self):
    article_headline = self.html.cssselect('meta[property="og:title"]')
    if article_headline: 
      return article_headline[0].get('content')

  def get_lede(self):
    description = self.html.cssselect('meta[name="description"]')
    if not description:
      description = self.html.cssselect('meta[property="og:description"]')

    if description: return description[0].get('content')

  def get_keywords(self):
    keywords = self.html.cssselect('meta[name="news_keywords"]')
    if not keywords:
      keywords = self.html.cssselect('meta[name="keywords"]')

    if keywords: return keywords[0].get('content')