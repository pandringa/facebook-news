from .base import JsonScraper, Article
import re

class NBCNewsScraper(JsonScraper):
  domains = ["www.nbcnews.com", "www.nbcolympics.com", "www.today.com", "collegebasketball.nbcsports.com"]
  category_map = {
    'Consumer': 'business',
    'better': 'lifestyle',
    'pop-culture': 'lifestyle',
    'us news': 'national',
    'europe': 'world',
    'education': 'national',
    'china': 'world',
    'north korea': 'world',
    'mach': 'science',
    'crime courts': 'national',
    'mideast': 'world',
    'airplane mode': 'lifestyle',
    'americas heroin epidemic': 'national',
    'bill cosby scandal': 'national',
    'charleston church shooting': 'national',
    'harvey weinstein scandal': 'national',
    'isis terror': 'world',
    'isis uncovered': 'world',
    'lethal injection': 'national',
    'puerto rico crisis': 'national',
    'sexual misconduct': 'national',
    'winter olympics 2018': 'sports',
    'think': 'opinion',
  }

  def get_category(self):
    if self.url.host == "www.nbcolympics.com" or 'nbcsports.com' in self.url.host:
      return 'sports'
    if self.url.host == "www.today.com":
      return 'lifestyle'

    category = super(NBCNewsScraper, self).get_category()
    if category and category != 'news':
      return category

    if self.url:
      slug = re.match('^\/([\w-]+)\/([\w-]+)\/', self.url.path)
      categories = []
      if slug:
        if slug.group(1):
          categories.append( slug.group(1) )
        if slug.group(2):
          categories.append( slug.group(2) )
        return '/'.join(categories)

  @classmethod
  def categorize(cls, a):
    if isinstance(a, Article):
      pub_cat = a.pub_category
    elif isinstance(a, str):
      pub_cat = a

    category = None
    if pub_cat and '/' in pub_cat:
      sub_cat = pub_cat.split('/')[1].replace('-', ' ')
      category = super(NBCNewsScraper, cls).categorize(sub_cat)
      if not category:
        top_cat = pub_cat.split('/')[0].replace('-', ' ')
        category = super(NBCNewsScraper, cls).categorize(top_cat)
      if category:
        return category

    return super(NBCNewsScraper, cls).categorize(a)