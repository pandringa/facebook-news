from lxml.html import fromstring

# Base Scraper for others to inherit from
class Scraper:
  domain = None

  def __init__(self, res_text):
    self.html = fromstring(res_text)

  def get_category():
    return 'Not Implemented'

  def get_date():
    return 'Not Implemented'

  def get_headline():
    return 'Not Implemented'

  def get_lede():
    return 'Not Implemented'

  def get_keywords():
    return 'Not Implemented'