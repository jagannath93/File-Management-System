# Django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.conf import settings
from django.template.loader import get_template
from django.template.context import Context
from django.utils.html import escape
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string
from django.contrib.messages.api import get_messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

# App Imports
from fms.models import *

# python imports
import os
import json
import StringIO

ALLOWED_USERS = ['shanmuk.mir@gmail.com', 'mansarch@gmail.com']


def login(request):
  return render_to_response('fms/login.html', RequestContext(request))

#@user_passes_test(lambda(u if u.username in ALLOWED_USERS))
@login_required
def home(request):
  """Login complete view, displays user data"""
  if request.user.email in ALLOWED_USERS:
    return render_to_response('fms/home.html', RequestContext(request))
  else:
    return HttpResponse("Access Denied!\n You don't have Permission to access this application!")

def error(request):
  """Error view"""
  messages = get_messages(request)
  return render_to_response('fms/error.html', RequestContext(request))

@login_required
def book_issued_slip(request, issue_id):
  if request.user.email in ALLOWED_USERS:
    try:
      issue = IssueBooks.objects.get(pk=issue_id)
      books = issue.issued_books.all()
      pdata = {'person_name': issue.person_name, 'person_email': issue.person_email, 'person_mobile_no': issue.person_mobile_no, \
              'person_group': issue.person_group, 'issue_date': str(issue.issue_date), 'return_date': str(issue.return_date), \
              'issue_id': str(issue.pk)}
      bdata = []
      for book in books:
        tmp = {'name': book.name, 'isbn_number': book.isbn_number, 'publisher': book.publisher, 'author': book.author, 'id': book.pk} 
        bdata.append(tmp)
      data = {'pdata': pdata, 'bdata': bdata}
      #return HttpResponse(json.dumps(data),  mimetype='application/json')
      return render_to_response('fms/book_issued_slip.html', data, RequestContext(request))
    except ObjectDoesNotExist:
      return HttpResponse('Invalid issue_id')
  else:
    return HttpResponse("Access Denied!\n You don't have Permission to access this application!")
   
@login_required
def issue_books(request):
  if request.user.email in ALLOWED_USERS:
    if request.method == 'GET' and request.is_ajax():
      person_name = request.GET.get('person_name')
      person_email = request.GET.get('person_email')
      person_group = request.GET.get('person_group')
      person_mobile_no = request.GET.get('person_mobile_no')
      issue_date = request.GET.get('issue_date')
      return_date = request.GET.get('return_date')
      books = request.GET.getlist('books')
      try:
        issue = IssueBooks.objects.get(person_name=person_name)
        issue.person_email = person_email
        issue.person_mobile_no = person_mobile_no
        issue.issue_date = issue_date
        issue.return_date = return_date
        issue.save()
        for book_id in books:
          book = Book.objects.get(pk=book_id)
          if not book in issue.issued_books.all() and book.avilability_status is True:
            issue.issued_books.add(book)
            book.avilability_status = False
            book.save()
        return HttpResponse('OK')
        #return HttpResponseRedirect(reverse('book_issued_slip', args=(issue.pk,)))
        #return HttpResponseRedirect('http://127.0.0.1:8000/fms/book_issued_slip/%s/' % str(issue.pk))
      except ObjectDoesNotExist:
        new_issue = IssueBooks(person_name=person_name, person_email=person_email, person_mobile_no=person_mobile_no, \
                    person_group=person_group, issue_date=issue_date, return_date=return_date)
        new_issue.save()
        for book_id in books:
          book = Book.objects.get(pk=book_id)
          if not book in new_issue.issued_books.all() and book.avilability_status is True:
            new_issue.issued_books.add(book)
            book.avilability_status = False
            book.save()
        return HttpResponse('OK')
        #return HttpResponseRedirect('/fms/book_issued_slip/'+str(issue.pk)+'/')
    else:
      return render_to_response('fms/issue_books.html', RequestContext(request))
  else:
    return HttpResponse("Access Denied!\n You don't have Permission to access this application!")

@login_required()
def book_search(request):
  """
    TODO: Add GET and is_ajax() restriction.
  """
  if request.user.email in ALLOWED_USERS:
    if request.method == 'GET' and request.is_ajax():
      q = request.GET.get('q')
      filter1 = request.GET.get('filter1') # Search-by: author, publisher, isbn etc
      filter2 = request.GET.get('filter2') # Search-by: Category   
      
      if q is not None:
        books = []

        # Filter2
        if not filter2 == '':
          cats = Category.objects.all()
          cat = Category.objects.get(name=filter2)
          if cat in cats:
            books_set = cat.category_books.all()
            books = books_set.all()
          else:
            return HttpResponse("Invalid filter!")
        else:
          books = Book.objects.all()

        # Filter1
        if not filter1 == '':
          if filter1 == 'name':
            books = books.filter(
                Q( name__icontains = q )
            )
          elif filter1 == 'author':
            books = books.filter(
                Q( author__icontains = q )
            )
          elif filter1 == 'publisher':
            books = books.filter(
                Q( publisher__icontains = q )
            )
          elif filter1 == 'isbn_number':
            books = books.filter(
                Q( isbn_number__icontains = q )
            )
          else:
            return HttpResponse("Invalid filter!")
        else:
          books = books.filter(
            Q( name__icontains = q )|
            Q( author__icontains = q )|
            Q( isbn_number__icontains = q )|
            Q( publisher__icontains = q )
          )  

        data = []
        for book in books[:10]:
          #address = {'rack': book.address.rack, 'row': book.address.row, 'shelf_set': book.address.shelf_set}
          tmp = {'name': book.name, 'code': book.code, 'isbn': str(book.isbn_number), 'id': str(book.pk), 'publisher': book.publisher, 'status': book.avilability_status, 'author': book.author, 'address': str(book.address), 'image': book.image.url}
          data.append(tmp)
        return HttpResponse(json.dumps(data),  mimetype='application/json')
      else:
        return HttpResponse(json.dumps([]),  mimetype='application/json')
    else:
      return render_to_response('fms/book-search.html', RequestContext(request))
  else:
    return HttpResponse("Access Denied!\n You don't have Permission to access this application!")

#@login_required()
def get_book_data(request):
  #if request.user.email in ALLOWED_USERS:
  if request.method == 'GET' and request.is_ajax():
    book_id = request.GET.get('book_id')
    book = Book.objects.get(pk=book_id)
    #address = {'rack': book.address.rack, 'row': book.address.row, 'shelf_set': book.address.shelf_set}
    bdata = {'name': book.name, 'code':book.code, 'isbn': str(book.isbn_number), 'id': str(book.pk), 'publisher': book.publisher, 'status': book.avilability_status, 'author': book.author, 'address': str(book.address), 'image': book.image.url}
    data = {'bdata': bdata}
    return HttpResponse(json.dumps(data),  mimetype='application/json')
  else:
      return HttpResponse(json.dumps([]),  mimetype='application/json')
  #else:
  #  return HttpResponse("Access Denied!\n You don't have Permission to access this application!")

def public_book_search(request):
  """
    TODO: Add GET and is_ajax() restriction.
  """
  if request.method == 'GET' and request.is_ajax():
    q = request.GET.get('q')
    filter1 = request.GET.get('filter1') # Search-by: author, publisher, isbn etc
    filter2 = request.GET.get('filter2') # Search-by: Category   
    
    if q is not None:
      books = []

      # Filter2
      if not filter2 == '':
        cats = Category.objects.all().exclude(name='Reference')
        cat = Category.objects.get(name=filter2)
        if cat in cats:
          books_set = cat.category_books.all()
          books = books_set.all()
        else:
          return HttpResponse("Invalid filter!")
      else:
        books = Book.objects.all()

      # Filter1
      if not filter1 == '':
        if filter1 == 'name':
          books = books.filter(
              Q( name__icontains = q )
          )
        elif filter1 == 'author':
          books = books.filter(
              Q( author__icontains = q )
          )
        elif filter1 == 'publisher':
          books = books.filter(
              Q( publisher__icontains = q )
          )
        elif filter1 == 'isbn_number':
          books = books.filter(
              Q( isbn_number__icontains = q )
          )
        else:
          return HttpResponse("Invalid filter!")
      else:
        books = books.filter(
          Q( name__icontains = q )|
          Q( author__icontains = q )|
          Q( isbn_number__icontains = q )|
          Q( publisher__icontains = q )
        )  

      data = []
      for book in books[:10]:
        #address = {'rack': book.address.rack, 'row': book.address.row, 'shelf_set': book.address.shelf_set}
        tmp = {'name': book.name, 'code': book.code, 'isbn': str(book.isbn_number), 'id': str(book.pk), 'publisher': book.publisher, 'status': book.avilability_status, 'author': book.author, 'address': str(book.address), 'image': book.image.url}
        data.append(tmp)
      return HttpResponse(json.dumps(data),  mimetype='application/json')
    else:
      return HttpResponse(json.dumps([]),  mimetype='application/json')
  else:
    return render_to_response('fms/public-book-search.html', RequestContext(request))

@login_required
def books_list(request):
  if request.user.email in ALLOWED_USERS:
    if request.method == 'GET' and request.is_ajax():
      try:
        category = request.GET.get('cat')
        if category is not None:
          cat = Category.objects.get(name=category)
          books = cat.category_books.all()
          bdata = []
          for book in books:
            tmp = {'name': book.name, 'code': book.code, 'isbn': str(book.isbn_number), 'id': str(book.pk), 'publisher': book.publisher,\
                    'status': book.avilability_status, 'author': book.author, 'image': book.image.url, 'address': str(book.address)}
            bdata.append(tmp)
          data = {'bdata': bdata}
          return HttpResponse(json.dumps(data), mimetype='application/json')
        else:
          books = Book.objects.all()
          bdata = []
          for book in books:
            tmp = {'name': book.name, 'code': book.code,'isbn': str(book.isbn_number), 'id': str(book.pk), 'publisher': book.publisher,\
                    'status': book.avilability_status, 'author': book.author, 'image': book.image.url, 'address': str(book.address)}
            bdata.append(tmp)
          data = {'bdata': bdata}
          return render_to_response('fms/books-list.html', data, RequestContext(request))
      except ObjectDoesNotExist:
        return HttpResponse('Invalid data error!')
    else:
      book_list = Book.objects.all()
      paginator = Paginator(book_list, 25)
      page = request.GET.get('page')
      if page is None:
        page = 1 
      books = paginator.page(page)

      #bdata = []
      #for book in books:
      #  tmp = {'name': book.name, 'isbn': str(book.isbn_number), 'id': str(book.pk), 'publisher': book.publisher,\
      #             'status': book.avilability_status, 'author': book.author, 'image': book.image.url}
      #  bdata.append(tmp)
      #data = {'bdata': bdata}
      return render_to_response('fms/books-list.html', {'books': books}, RequestContext(request))
  else:
    return HttpResponse("Access Denied!\n You don't have Permission to access this application!")

@login_required
def list_book_issues(request):
  if request.user.email in ALLOWED_USERS:
    try:
      issues = IssueBooks.objects.all()
      data = []
      for issue in issues:
        books = issue.issued_books.all()
        if len(books) is not 0:
          pdata = {'person_name': issue.person_name, 'person_email': issue.person_email, 'person_mobile_no': issue.person_mobile_no, \
                  'person_group': issue.person_group, 'issue_date': str(issue.issue_date), 'return_date': str(issue.return_date), \
                  'issue_id': str(issue.pk)}
          bdata = []
          for book in books:
            tmp = {'name': book.name, 'isbn_number': book.isbn_number, 'publisher': book.publisher, 'author': book.author, 'id': book.pk} 
            bdata.append(tmp)
          idata = {'pdata': pdata, 'bdata': bdata}
          data.append(idata)
          #return HttpResponse(json.dumps(data),  mimetype='application/json')
      return render_to_response('fms/list-all-book-issues.html', {'issues': data}, RequestContext(request))
    except e as Exception:
      return HttpResponse('Error occured!')
  else:
    return HttpResponse("Access Denied!\n You don't have Permission to access this application!")

@login_required
def get_book_issued_data(request):
  if request.user.email in ALLOWED_USERS:
    if request.method == 'GET' and request.is_ajax():
      try:
        issue_id = request.GET.get('issue_id')
        issue = IssueBooks.objects.get(pk=issue_id)
        books = issue.issued_books.all()
        pdata = {'person_name': issue.person_name, 'person_email': issue.person_email, 'person_mobile_no': issue.person_mobile_no, \
                'person_group': issue.person_group, 'issue_date': str(issue.issue_date), 'return_date': str(issue.return_date), \
                'issue_id': str(issue.pk)}
        bdata = []
        for book in books:
          tmp = {'name': book.name, 'isbn_number': book.isbn_number, 'publisher': book.publisher, 'author': book.author, 'id': book.pk} 
          bdata.append(tmp)
        data = {'pdata': pdata, 'bdata': bdata}
        return HttpResponse(json.dumps(data),  mimetype='application/json')
      except ObjectDoesNotExist:
        return HttpResponse('Invalid issue_id')
    else:
      return render_to_response('fms/issue_books.html', RequestContext(request))
  else:
    return HttpResponse("Access Denied!\n You don't have Permission to access this application!")

@login_required
def submit_books(request):
  if request.user.email in ALLOWED_USERS:
    if request.method == 'GET' and request.is_ajax():
      print request.GET
      try:
        issue_id = request.GET.get('issue_id')
        issue = IssueBooks.objects.get(pk=issue_id)
        books = issue.issued_books.all()
        for book in books:
          tmp = 'book_'+str(book.pk)
          if request.GET.get(tmp):
            if request.GET.get(tmp) == 'on':
              issue.issued_books.remove(book)
              book.avilability_status = True
              book.save()
        return HttpResponse('ok')
      except ObjectDoesNotExist:
        return HttpResponse('Invalid issue_id')
 


      """
      issue_date = request.GET.get('issue_date')
      return_date = request.GET.get('return_date')
      books = request.GET.getlist('books')
      try:
        issue = IssueBooks.objects.get(person_name=person_name)
        for book_id in books:
          book = Book.objects.get(pk=book_id)
          if not book in issue.issued_books.all():
            issue.issued_books.add(book)
        return HttpResponse('OLD')
      except ObjectDoesNotExist:
        new_issue = IssueBooks(person_name=person_name, person_email=person_email, person_mobile_no=person_mobile_no, \
                    person_group=person_group, issue_date=issue_date, return_date=return_date)
        new_issue.save()
        for book_id in books:
          book = Book.objects.get(pk=book_id)
          if not book in new_issue.issued_books.all():
            new_issue.issued_books.add(book)
        return HttpResponse('NEW')
        """
    else:
      page_msg = request.GET.get('page_msg')
      if page_msg is not None:
        return render_to_response('fms/submit_books.html', {'page_msg': page_msg}, RequestContext(request))
      else:
        return render_to_response('fms/submit_books.html', RequestContext(request))
  else:
    return HttpResponse("Access Denied!\n You don't have Permission to access this application!")

@login_required
def issued_persons_search(request):
  if request.user.email in ALLOWED_USERS:
    q = request.GET.get('q')
    if q is not None:
      issued_persons = IssueBooks.objects.filter(
        Q( person_name__icontains = q )|
        Q( person_email__icontains = q )|
        Q( person_mobile_no__icontains = q )|
        Q( person_group__icontains = q )
      )

      data = []
      for person in issued_persons:
        tmp = {'name': person.person_name, 'group': person.person_group, 'email': person.person_email, 'mobile_no': person.person_mobile_no, 'id': str(person.pk), 'issue_date': str(person.issue_date), 'return_date': str(person.return_date) }
        data.append(tmp)
      return HttpResponse(json.dumps(data),  mimetype='application/json')
    else:
      return HttpResponse(json.dumps([]),  mimetype='application/json')
  else:
    return HttpResponse("Access Denied!\n You don't have Permission to access this application!")

@login_required
def search_books(request):
  if request.user.email in ALLOWED_USERS:
    q = request.GET.get('q')
    if q is not None:
      books = Book.objects.filter(
        Q( name__icontains = q )|
        Q( author__icontains = q )|
        Q( isbn_number__icontains = q )|
        Q( publisher__icontains = q )
      )
      data = []
      for book in books:
        tmp = {'name': book.name, 'code': book.code, 'isbn': str(book.isbn_number), 'id': str(book.pk), 'publisher': book.publisher, 'status': book.avilability_status, 'author': book.author, 'address': str(book.address), 'image': book.image.url}
        data.append(tmp)
      return HttpResponse(json.dumps(data),  mimetype='application/json')
    else:
      return HttpResponse(json.dumps([]),  mimetype='application/json')
  else:
    return HttpResponse("Access Denied!\n You don't have Permission to access this application!")
