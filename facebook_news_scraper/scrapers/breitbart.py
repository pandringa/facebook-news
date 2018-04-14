from .base import JsonScraper
from .base import Article

class BreitbartScraper(JsonScraper):
  domains = ["www.breitbart.com"]
  category_map = {
    '2nd amendment': 'national',
    'abortion': 'national',
    'donald trump': 'politics',
    'white house': 'politics',
    'republicans': 'politics',
    'democrats': 'politics',
    'cpac': 'politics',
    'law enforcement': 'national',
    'big hollywood': 'lifestyle',
    'south korea': 'world',
    'breitbart sports': 'sports',
    'medicine': 'lifestyle',
    'big journalism': 'politics',
    'breitbart london': 'world',
    'breitbart jerusalem': 'world',
    'middle east': 'world',
    'economics': 'national',
    'breitbart texas': 'national',
    'obama': 'politics',
    'hillary clinton': 'politics',
    'breitbart california': 'politics',
    'border': 'national',
    'north korea': 'world',
    'united kingdom': 'world',
    'tim kaine': 'politics',
    'bernie sanders': 'politics',
    'education': 'national',
  }
  headline_keywords = {
    'Vice President': 'politics',
    'President Trump': 'politics',
    'President Donald Trump': 'politics',
    'Sen.': 'politics',
    'Rep.': 'politics',
    'Senator': 'politics',
    'Representative': 'politics',
    'politics': 'politics',
    'police': 'national',
    'Trump': 'politics',
    'oscars': 'entertainment',
    'white house': 'politics',
    'election': 'politics',
    'democrat': 'politics',
    'democratic': 'politics',
    'republican': 'politics',
    'joe biden': 'politics',
  }

  def get_category(self):
    section = self.html.cssselect('[property="article:categories"]')
    if not section:
      section = self.html.cssselect('[property="article:section"]')
    
    if section:
      return section[0].get('content')
    return super(BreitbartScraper, self).get_category()

  def get_keywords(self):
    if self.json_metadata and 'keywords' in self.json_metadata:
      return self.json_metadata['keywords']

    return super(BreitbartScraper, self).get_keywords()

  @classmethod
  def categorize(cls, a):
    category = super(BreitbartScraper, cls).categorize(a)
    if category:
      return category

    if isinstance(a, Article) and a.pub_category and ',' in a.pub_category:
      first_guess = a.pub_category.split(',')[-1]
      first_guess = super(BreitbartScraper, cls).categorize(first_guess)
      if first_guess:
        return first_guess
      guess = cls.try_guesses(a.pub_category)
      if guess:
        return guess

    if isinstance(a, Article) and a.pub_keywords:
      guess = cls.try_guesses(a.pub_keywords)
      if guess:
        return guess

    if isinstance(a, Article) and a.pub_headline:
      for word, category in cls.headline_keywords.items():
        if word.lower() in a.pub_headline.lower():
          return category
