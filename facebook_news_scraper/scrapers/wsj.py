from .base import Scraper

class WSJScraper(Scraper):
  domains = ["www.wsj.com", "partners.wsj.com"]

  def get_category(self):
    if self.url.host == 'partners.wsj.com':
      return 'Advertisement'
    article_section = self.html.cssselect('head meta[name="article.section"]')
    
    if article_section: 
      return article_section[0].get('content')
    else:
      return super(WSJScraper, self).get_category()

  def get_date(self):
    article_published = self.html.cssselect('head meta[name="article.published"]')
    if not article_published:
      article_published = self.html.cssselect('[itemprop="datePublished"]')
    if article_published: 
      return article_published[0].get('content')

    return super(WSJScraper, self).get_date()

  def get_headline(self):
    article_headline = self.html.cssselect('head meta[name="article.headline"]')

    if article_headline: 
      return article_headline[0].get('content')
    else:
      return super(WSJScraper, self).get_headline()

  def get_lede(self):
    article_summary = self.html.cssselect('head meta[name="article.summary"]')
    if article_summary: 
      return article_summary[0].get('content')
    else:
      return super(WSJScraper, self).get_lede()