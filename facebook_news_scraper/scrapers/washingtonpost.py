from .base import JsonScraper, tzs
import re
from dateutil.parser import parse as parse_date

class WashingtonPostScraper(JsonScraper):
  domains = ["www.washingtonpost.com"]
  category_map = {
    'the fix': 'politics',
    'post nation': 'national',
    'post politics': 'politics',
    'worldviews': 'world',
    'animalia': 'science',
    'speaking of science': 'science',
    'blogs': 'opinion',
    'powerpost': 'politics',
    'goingoutguide': 'lifestyle',
    'going out guide': 'lifestyle',
    'acts of faith': 'lifestyle',
    'capital weather gang': 'local',
    'early lead': 'sports',
    'fact checker': 'politics',
    'global opinions': 'opinion',
    'solo-ish': 'lifestyle',
    'to your health': 'lifestyle',
    'true crime': 'national',
    'outlook': 'opinion',
    'answer sheet': 'national',
    'comic riffs': 'lifestyle',
    'd.c. sports blog': 'lifestyle',
    'democracypost': 'opinion',
    'grade point': 'national',
    'gridlock': 'national',
    'made by history': 'opinion',
    'checkpoint': 'national',
    'on parenting': 'lifestyle',
    'reliable source': 'lifestyle',
  }

  def get_category(self):
    result = ""
    match = re.search('^/(\w+)/.*', self.url.path)
    if match and match.group(1):
      result += match.group(1) + ' - '

    category_link = self.html.cssselect('section#top-content .headline-kicker a.kicker-link')
    if category_link:
      result += category_link[0].text_content()

    if result:
      return result  
    return super(WashingtonPostScraper,self).get_category()

  def get_date(self):
    date = super(WashingtonPostScraper,self).get_date()
    if not date:
      date = self.html.cssselect('[itemprop="datePublished"]')
      if date and date[0].get('content'):
        try:
          py_date = parse_date(date[0].get('content'), tzinfos=tzs)
          return py_date
        except:
          print("Error parsing date in WashingtonPostScraper: %s (url: %s)" % (date[0].get('content'), self.url))
    else:
      return date


  @classmethod
  def categorize(cls, a):
    if a.pub_category:
      category = re.match('([\w\s]+)\s*-\s*([\w\s]+)?', a.pub_category)
      if category:
        if category.group(1).strip() == 'news' and category.group(2):
          category = category.group(2).lower().strip()
        else:
          category = category.group(1).lower().strip()
        return super(WashingtonPostScraper, cls).categorize(category)
      
      return super(WashingtonPostScraper, cls).categorize(a)
