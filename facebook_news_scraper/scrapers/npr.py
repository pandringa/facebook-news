import json
from .base import Scraper

class NPRScraper(Scraper):
  domains = ["www.npr.org"]

  def get_category(self):
    category_string = ""

    toplevel_section = self.html.cssselect('header.contentheader[data-metrics]')
    if toplevel_section:
      try:
        json_section = json.loads(toplevel_section[0].get('data-metrics'))
        category_string += json_section['category']
      except:
        pass

    article_section = self.html.cssselect('article h3.slug')
    if article_section: 
      if toplevel_section: category_string += ' - '
      category_string += article_section[0].text_content().strip()

    return category_string or None

  def get_date(self):
    dateblock_time = self.html.cssselect('article #story-meta .dateblock time')
    if dateblock_time:
      return dateblock_time[0].get('datetime')

    return super(NPRScraper, self).get_date()

  def get_headline(self):
    generic_headline = super(NPRScraper, self).get_headline()
    if generic_headline: return generic_headline

    story_title = self.html.cssselect('article .storytitle h1')
    if story_title:
      return story_title.text_content().strip()

  def get_keywords(self):
    keywords = super(NPRScraper, self).get_keywords()
    if not keywords:
      tags = self.html.cssselect('article .tags li')
      if tags: 
        keywords = ','.join([t.text_content().strip() for t in tags])
    
    return keywords
