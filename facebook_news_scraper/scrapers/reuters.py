from .base import Scraper

class ReutersScraper(Scraper):
  domains = ["www.reuters.com"]

  def get_category(self):
    article_section = self.html.cssselect('meta[name="DCSext.DartZone"]')
    if not article_section:
      article_section = self.html.cssselect('meta[name="analyticsAttributes.contentChannel"]')
    if not article_section:
      article_section = self.html.cssselect('meta[property="og:article:section"]')

    if article_section: 
      return article_section[0].get('content')
    else:
      return super(ReutersScraper, self).get_category()

  def get_date(self):
    article_published = self.html.cssselect('meta[name="analyticsAttributes.articleDate"]')
    if not article_published:
      article_published = self.html.cssselect('meta[name="sailthru.date"]')
    if not article_published:
      article_published = self.html.cssselect('meta[property="og:article:published_time"]')

    if article_published: 
      return article_published[0].get('content')
    else:
      return super(ReutersScraper, self).get_date()

  def get_headline(self):
    article_headline = self.html.cssselect('meta[name="analyticsAttributes.contentTitle"]')
    if not article_headline:
      article_headline = self.html.cssselect('meta[name="sailthru.title"]')
    
    if article_headline: 
      return article_headline[0].get('content')
    else:
      return super(ReutersScraper, self).get_headline()

  def get_keywords(self):
    keywords = super(ReutersScraper, self).get_keywords()
    
    if keywords and ';' in keywords:
      return ','.join(keywords.split(';'))
    return keywords 
