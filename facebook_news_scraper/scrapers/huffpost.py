from .base import JsonScraper

class HuffingtonPostScraper(JsonScraper):
  domains = ["www.huffingtonpost.com"]
  category_map = {
    'huffpost personal': 'opinion',
    'own': 'lifestyle',
  }