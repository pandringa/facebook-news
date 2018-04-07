from .base import JsonScraper

class CBSNewsScraper(JsonScraper):
  domains = ["www.cbsnews.com"]

  def get_category(self):
    if self.json_metadata and 'articleSection' in self.json_metadata: 
        return ' - '.join(self.json_metadata['articleSection'])
    return super(CBSNewsScraper, self).get_category()
