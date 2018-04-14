import json
from .base import Scraper
import re

class NPRScraper(Scraper):
  domains = ["www.npr.org"]
  category_map = {
    'all songs considered': 'lifestyle',
    'all tech considered': 'business',
    '13.7: cosmos and culture': 'science',
    'arts & life': 'lifestyle',
    'author interviews': 'lifestyle',
    'brave new workers': 'business',
    'criminal justice collaborative': 'national',
    'first listen': 'lifestyle',
    'goats and soda': 'world',
    'monkey see': 'lifestyle',
    'movie interviews': 'lifestyle',
    'npr ed': 'national',
    'parallels': 'world',
    'planet money': 'business',
    'politics: fact check': 'politics',
    'politics: member stations': 'politics',
    'shots': 'lifestyle',
    'storycorps': 'lifestyle',
    'the record': 'lifestyle',
    'the rise of the contract workers': 'business',
    'the salt': 'lifestyle',
    'the torch': 'sports',
    "the week's best stories from npr books": 'lifestyle',
    'tiny desk': 'lifestyle',
    'turning the tables': 'lifestyle',
    'world cafe': 'lifestyle',
    'book news & features': 'lifestyle',
    'deceptive cadence': 'lifestyle',
    'music interviews': 'lifestyle',
    'songs we love': 'lifestyle',
    'law': 'national',
  }


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

  @classmethod
  def categorize(cls, a):
    if a.pub_category:
      if '13.7: Cosmos And Culture' in a.pub_category:
        return 'science'
      elif 'The Two-Way' in a.pub_category:
        category = re.match('The Two-Way\s?-?([\d\w\s:&\.]+)?', a.pub_category)
      else:  
        category = re.match('([\d\w\s:&\']+)-?([\d\w\s:&\.\']+)?', a.pub_category)
      
      if category and category.group(1):
        category = category.group(1).lower().strip()
        return super(NPRScraper, cls).categorize(category)
      
    return super(NPRScraper, cls).categorize(a)

