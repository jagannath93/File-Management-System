from django.db import models
from fms import constants as FC
from django.utils import timezone
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist

#import datetime

class Category(models.Model):
  name = models.CharField(max_length=30, null=False, blank=False)

  def __unicode__(self):
    return self.name

class Book(models.Model):
  name = models.CharField(max_length=100, null=False, blank=False)
  code = models.CharField(max_length=15, null=True, blank=True)
  categories = models.ManyToManyField('Category', related_name='category_books')
  author = models.CharField(max_length=60, null=True, blank=True)
  publisher = models.CharField(max_length=60, null=True, blank=True)
  isbn_number = models.CharField(max_length=25, null=True, blank=True)
  address = models.ForeignKey('BookAddress')
  avilability_status = models.BooleanField(default=True, null=False, blank=False)
  added_on = models.DateTimeField(null=False, editable=False)
  last_updated = models.DateTimeField(null=False, editable=False)
  image = models.ImageField(upload_to = 'media/books/', default = 'media/thumbnail.png') 
          #models.ForeignKey('Image', related_name='images', null=True)

  def __unicode__(self):
    return self.name

  def save(self, *args, **kwargs):
    if not self.id:
      self.added_on = timezone.now()
      """"
      if not self.image:
        try:
          print "try"
          default_image = Image.objects.get(img = File(open('media/books/thumbnail.png')))
        except ObjectDoesNotExist:
          print "except"
          default_image = Image(img = File(open('media/thumbnail.png')))
          default_image.save()
        self.image = default_image
        print self.image
     """
    self.last_updated = timezone.now()
    return super(Book, self).save(*args, **kwargs)

class BookAddress(models.Model):
  rack = models.CharField(max_length=15, null=True, blank=True)
  row = models.CharField(max_length=10, null=True, blank=True)
  shelf_set = models.CharField(max_length=10, null=True, blank=True)

  def __unicode__(self):
    return self.rack

"""
class Image(models.Model):
  #name = models.CharField(max_length=10, null=False, blank=False)
  img = models.ImageField(upload_to = 'media/books/', default = 'media/books/thumbnail.png') 

  def __unicode__(self):
    return self.img.url
"""

class IssueBooks(models.Model):
  person_name = models.CharField(max_length=60, null=False, blank=False)
  person_email = models.EmailField(null=True, blank=True)
  person_mobile_no = models.CharField(max_length=15, null=True, blank=True)
  person_group = models.CharField(max_length=10, choices=FC.PERSON_GROUPS, null=False, blank=False)
  issue_date = models.DateField(null=False, blank=False, default=timezone.now()) 
  return_date = models.DateField(null=True, blank=True, default=timezone.now()+timezone.timedelta(7))
  issued_books = models.ManyToManyField('Book', null=True)
  is_submitted_all_books = models.BooleanField(default=False)

  def __unicode__(self):
    return self.person_group+": "+self.person_name