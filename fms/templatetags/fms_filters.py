from django import template

register = template.Library()

@register.filter
def get_range(pages):
  if pages:
    return range(1, int(pages)+1)
  else:
    return []

@register.filter
def format_val(arg):
  if arg is not None:
    if arg == True:
      return "YES"
    elif arg == False:
      return "NO"
    elif arg == "null":
      return "--"
    else:
      return arg
  else:
    return "--"

@register.filter
def format_book_cat(book):
  cats = book.categories.all()
  categories = ''
  for cat in cats:
    categories += cat.name
    if len(cats) > 1:
      categories += ", "
  return categories
