from django.contrib import admin
from fms.models import *

class BookAdmin(admin.ModelAdmin):
  list_filter = ('name', 'isbn_number', 'category', 'publisher', 'address')
  search_fields = ['name', 'isbn_number', 'category', 'publisher', 'address']

admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(BookAddress)
admin.site.register(IssueBooks)

