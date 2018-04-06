from .base import Scraper

class ReutersScraper(Scraper):
  domain = "www.reuters.com"

  def get_category(self):
    article_section = self.html.cssselect('meta[name="DCSext.DartZone"]')
    if not article_section:
      article_section = self.html.cssselect('meta[name="analyticsAttributes.contentChannel"]')
    if not article_section:
      article_section = self.html.cssselect('meta[property="og:article:section"]')

    if article_section: return article_section[0].get('content')

  def get_date(self):
    article_published = self.html.cssselect('meta[name="analyticsAttributes.articleDate"]')
    if not article_published:
      article_published = self.html.cssselect('meta[name="sailthru.date"]')
    if not article_published:
      article_published = self.html.cssselect('meta[property="og:article:published_time"]')

    if article_published: return article_published[0].get('content')

  def get_headline(self):
    article_headline = self.html.cssselect('meta[name="analyticsAttributes.contentTitle"]')
    if not article_headline:
      article_headline = self.html.cssselect('meta[name="sailthru.title"]')
    if not article_headline:
      article_headline = self.html.cssselect('meta[property="og:title"]')

    if article_headline: return article_headline[0].get('content')

  def get_lede(self):
    article_summary = self.html.cssselect('meta[name="description"]')
    if not article_summary:
      article_summary = self.html.cssselect('meta[property="og:description"]')
    
    if article_summary: return article_summary[0].get('content')

  def get_keywords(self):
    keywords = self.html.cssselect('meta[name="news_keywords"]')
    if not keywords:
      keywords = self.html.cssselect('meta[name="keywords"]')
    if not keywords:
      keywords = self.html.cssselect('meta[property="og:article:tag"]')

    if keywords:
      keywords = keywords[0].get('content')
      if ';' in keywords:
        return ','.join(keywords.split(';'))
      else:
        return keywords 
