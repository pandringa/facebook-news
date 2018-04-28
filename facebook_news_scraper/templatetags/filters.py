from django.template import Library

register = Library()

@register.filter
def get_item(obj, key):
  return getattr(obj, key)

@register.filter
def get_count(post, reaction):
  return getattr(post, reaction+'_count')

@register.filter
def get_headline(reaction):
  if reaction == 'comment':
    return 'Commented'
  elif reaction == 'share':
    return 'Shared'
  else:
    return "'"+reaction+"'-ed"