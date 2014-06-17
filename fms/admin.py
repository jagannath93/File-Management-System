from django.contrib import admin
from fms.models import *

class BookAdmin(admin.ModelAdmin):
  list_filter = ('name', 'code', 'isbn_number', 'author', 'publisher')
  search_fields = ['name', 'code', 'isbn_number', 'author', 'publisher']

admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(BookAddress)
admin.site.register(IssueBooks)

