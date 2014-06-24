from django.contrib import admin
from fms.models import *

class BookAdmin(admin.ModelAdmin):
  list_filter = ('name', 'code', 'isbn_number', 'author', 'publisher')
  search_fields = ['name', 'code', 'isbn_number', 'author', 'publisher']

class DocumentAdmin(admin.ModelAdmin):
  list_filter = ('name',)
  search_fields = ['name']
  fieldsets = (
    (None, {
        'fields': ('name', 'cat', 'subcat1', 'subcat2', 'document_number', 'address', 'rack', 'avilability_status', 'added_on', 'last_updated')
    }),
  )

  def get_readonly_fields(self, request, obj = None):
    if obj: #In edit mode
        return ('address', 'added_on', 'last_updated') + self.readonly_fields
    return self.readonly_fields

admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(BookAddress)
admin.site.register(IssueBooks)

admin.site.register(DocumentCategory)
admin.site.register(DocumentSubCategory1)
admin.site.register(DocumentSubCategory2)
admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentRack)
admin.site.register(DocumentRackImage)
