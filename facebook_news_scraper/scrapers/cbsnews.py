from .base import JsonScraper, Article

class CBSNewsScraper(JsonScraper):
  domains = ["www.cbsnews.com"]
  category_map = {
    'u.s.': 'national',
    'donald trump': 'politics',
    'moneywatch': 'business',
    'markets': 'business',
    'scitech': 'science',
    'health & science': 'science',
    '60 minutes politics': 'politics',
    'sunday morning': 'lifestyle',
    'face the nation': 'politics',
    'crimesider': 'national',
    'florida shooting': 'national',
    'google': 'business',
    'NBA': 'sports'
  }
  keyword_categories = {
    '2018 Winter Olympic Games': 'sports',
    'california': 'national',
    'Donald Trump': 'politics',
    'entertainment': 'lifestyle',
    'florida shooting': 'national',
    'immigration': 'national',
    'nfl': 'sports',
    'north korea': 'world',
    'Politics': 'politics',
    'sarah sanders': 'politics',
    'saudi arabia': 'world',
    'U.S.': 'national',
    'united kingdom': 'world',
    'World': 'world',
  }


  def get_category(self):
    if self.json_metadata and 'articleSection' in self.json_metadata: 
        return ' - '.join(self.json_metadata['articleSection'])
    return super(CBSNewsScraper, self).get_category()

  @classmethod
  def categorize(cls, a):
    category = None
    if isinstance(a, Article) and a.pub_category and '-' in a.pub_category:
      categories = a.pub_category.split(' - ')
      top_cat = categories[0]
      sub_cat = categories[1]
      category = super(CBSNewsScraper, cls).categorize(top_cat)
      if not category:
        category = super(CBSNewsScraper, cls).categorize(sub_cat)
    
    if not category:
      category = super(CBSNewsScraper, cls).categorize(a)

    if not category and isinstance(a, Article) and a.pub_category:
      if '60 Minutes' in a.pub_category or 'CBS This Morning' in a.pub_category or 'CBS Evening News' in a.pub_category or 'CBSN Originals' in a.pub_category:
        keywords = sorted(cls.keyword_categories.keys())
        pub_keywords = a.pub_keywords.split(',')
        for word in keywords:
          if word in pub_keywords:
            return cls.keyword_categories[word]

    if category:
      return category

    # if isinstance(a, Article) and a.pub_keywords and ',' in a.pub_keywords:
    #   guess = cls.try_guesses(a.pub_keywords)
    #   if guess:
    #     return guess