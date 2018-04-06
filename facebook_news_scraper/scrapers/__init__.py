import sys,inspect,os
from .wsj import WSJScraper

by_domain = {}

# Dynamically load in classes from other files in this directory
for module in os.listdir(os.path.dirname(__file__)):
  if module != '__init__.py' and module[-3:] == '.py':
    module_name = module[:-3]
    import_name = '%s.%s' % (__name__, module_name)

    __import__(import_name, globals(), locals(), ['*'])

    scrapers = inspect.getmembers(sys.modules[import_name], lambda member: inspect.isclass(member) and member.__module__.startswith(__name__) and member.domains )
    for s in scrapers:
      for d in s[1].domains:
        by_domain[d] = s[1]
