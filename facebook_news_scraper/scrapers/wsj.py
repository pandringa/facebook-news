from .base import Scraper

class WSJScraper(Scraper):
  domain = "www.wsj.com"

  def get_category(self):
    article_section = self.html.cssselect('head meta[name="article.section"]')
    
    if article_section: return article_section[0].get('content')

  def get_date(self):
    article_published = self.html.cssselect('head meta[name="article.published"]')
    if not article_published:
      article_published = self.html.cssselect('head meta[itemprop="datePublished"]')

    if article_published: return article_published[0].get('content')

  def get_headline(self):
    article_headline = self.html.cssselect('head meta[name="article.headline"]')

    if article_headline: return article_headline[0].get('content')

  def get_lede(self):
    article_summary = self.html.cssselect('head meta[name="article.summary"]')
    if not article_summary:
      article_summary = self.html.cssselect('head meta[name="description"]')
    
    if article_summary: return article_summary[0].get('content')

  def get_keywords(self):
    keywords = self.html.cssselect('head meta[name="news_keywords"]')
    if not keywords:
      keywords = self.html.cssselect('head meta[name="keywords"]')

    if keywords: return keywords[0].get('content')