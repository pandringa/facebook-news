from .base import JsonScraper

class GuardianScraper(JsonScraper):
  domains = ["www.theguardian.com"]
  category_map = {
    'global': 'lifestyle',
    'society': 'national',
    'uk news': 'national',
  }

  @classmethod
  def categorize(cls, a):
    category = super(GuardianScraper, cls).categorize(a)
    if not category and a.pub_keywords:
      category_guess = a.pub_keywords.split(',')[-1]
      return super(GuardianScraper, cls).categorize(category_guess)
    else:
      return category